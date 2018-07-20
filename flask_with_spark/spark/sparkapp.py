import os
import datetime
from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession, Row, DataFrame, Column
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml.feature import StringIndexer, IndexToString
from pyspark.sql import Row
from pyspark.ml import PipelineModel
from utilities.common import utc_now_ts as now
from utilities.similarity import compute_item_similarity
from shopping.models import Review
from flask import current_app as app


class SparkApp(object):
    def __init__(self, executor_memory="2560m", master_uri=None, mongo_uri=None,
                 deploy_mode="cluster"):
        self.executor_memory = executor_memory
        self.master_uri = app.config.get("SPARK_MASTER_URI") if master_uri is \
            None else master_uri
        self.deploy_mode = deploy_mode
        self.MONGO_URI = app.config.get("MONGODB_SETTINGS").get("host") \
            if mongo_uri is None else mongo_uri

    def create_spark_app(self):
        # Set SparkSession Object to run spark app
        spark = SparkSession.\
            builder.\
            master(self.master_uri).\
            config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.2.3").\
            getOrCreate()
        self.spark = spark

    def return_col(self, col_name="products"):
        col_uri = self.MONGO_URI + "." + col_name
        col_obj = self.spark.read\
            .format("com.mongodb.spark.sql.DefaultSource")\
            .option("uri", col_uri)\
            .load()
        col_obj.createOrReplaceTempView(col_name)
        return col_obj

    def return_all_books(self):
        self.create_spark_app()
        products = self.return_col(col_name="products")
        # Get distinct book names of all books
        book_names = products\
            .select("title")\
            .where(F.col("title").isNotNull())\
            .distinct()
        # Save Data to MongoDB
        book_names_uri = self.MONGO_URI + ".product_name"
        book_names.write\
            .format("com.mongodb.spark.sql.DefaultSource")\
            .mode("overwrite")\
            .option("uri", book_names_uri)\
            .save()
        self.spark.stop()

    def return_best_books(self, minimum_count=10, limit_count=10):
        self.create_spark_app()
        products = self.return_col(col_name="products")
        reviews = self.return_col(col_name="reviews")
        grouped = reviews\
            .groupBy("asin")\
            .agg(F.count("asin").alias("cnt"), F.avg("overall").alias("avgOverall"))\
            .sort(F.desc("avgOverall"), F.desc("cnt"))\
            .select("asin", "avgOverall", "cnt")\
            .filter(F.col("cnt") >= minimum_count)\
            .limit(limit_count)
        grouped.cache()
        bestReviews = grouped.alias('g')\
            .join(
                products.alias('p'),
                F.col("g.asin") == F.col("p.asin")
                )\
            .select(
                F.col("g.asin").alias("asin"),
                F.col("g.avgOverall").alias("ao"),
                F.col("p.title").alias("t"),
                F.col("p.price").alias("p"),
                F.col("p.imUrl").alias("iu"),
                F.col("p.description").alias("d"),
                F.col("g.cnt").alias("cnt"),
                )
        createdDate = now()
        bestReviews_with_dates = bestReviews.withColumn(
            "cd",
            F.lit(createdDate)
            )
        best_product_uri = self.MONGO_URI + ".best_product"
        bestReviews_with_dates.write\
            .format("com.mongodb.spark.sql.DefaultSource")\
            .mode("append")\
            .option("uri", best_product_uri)\
            .save()
        self.spark.catalog.clearCache()
        self.spark.stop()

    def make_recommendation_model(self):
        self.create_spark_app()
        reviews = self.return_col(col_name="reviews")
        users = self.return_col(col_name="user")
        selectedDf = reviews\
            .select("reviewerID", "asin", "overall")

        '''
        Make string indexer to convert string to index
        to make no error in ALS model
        '''

        reviewerIndexer = StringIndexer(
            inputCol="reviewerID",
            outputCol="userCol",
            handleInvalid="keep"
            )
        productIndexer = StringIndexer(
            inputCol="asin",
            outputCol="itemCol",
            handleInvalid="keep"
            )
        reviewStringModel = reviewerIndexer.fit(selectedDf)
        selectedDf = reviewStringModel.transform(selectedDf)
        reviewer_labels = reviewStringModel.labels
        productStringModel = productIndexer.fit(selectedDf)
        product_labels = productStringModel.labels
        transformedFeatures = productStringModel.transform(selectedDf)

        # Develop Model
        als = ALS(
            maxIter=10, regParam=0.01, userCol="userCol",
            itemCol="itemCol", ratingCol="overall",
            coldStartStrategy="nan"
              )
        alsModel = als.fit(transformedFeatures)

        # Only make recommendation for active users
        activeUsers = [x.e for x in users.select("e").collect()]
        selectedData = transformedFeatures[transformedFeatures
                                           .reviewerID.isin(activeUsers)]

        # make reverse tarnsform to productID and userID
        num_recommends = 10
        recommendationData = alsModel.recommendForUserSubset(
            selectedData,
            num_recommends
            )
        product_labels_ = F.array(*[F.lit(x) for x in product_labels])
        recommendations = F.array(*[F.struct(
            product_labels_[F.col("recommendations")[i]["itemCol"]].alias("itemCol"),
            F.col("recommendations")[i]["rating"].cast("double").alias("rating")
        ) for i in range(num_recommends)])

        recommendationData = recommendationData\
            .withColumn("recommendations", recommendations)
        userReverse = IndexToString(
            inputCol="userCol",
            outputCol="reviewerID",
            labels=reviewer_labels
            )
        recommendationData = userReverse\
            .transform(recommendationData)\
            .select("reviewerID", "recommendations")

        createdDate = now()
        recommendationData = recommendationData.withColumn(
            "dc",
            F.lit(createdDate)
        )
        # Save data to mongodb
        col_name = self.MONGO_URI + ".recommendation_table"
        recommendationData.write\
            .format("com.mongodb.spark.sql.DefaultSource")\
            .mode("append")\
            .option("uri", col_name)\
            .save()

        self.spark.catalog.clearCache()
        self.spark.stop()

    def make_similarity_table(self):
        self.create_spark_app()
        reviews = self.return_col(col_name="reviews")
        selectedDf = reviews\
            .select("reviewerID", "asin", "overall")

        itemBased = compute_item_similarity(selectedDf, user_col='reviewerID',
                                            item_col='asin', rating_col='overall',
                                            method='cosine', use_persist=False)

        col_name = self.MONGO_URI + ".similarity_table"
        itemBased.write\
            .format("com.mongodb.spark.sql.DefaultSource")\
            .mode("overwrite")\
            .option("uri", col_name)\
            .save()

    def load_model(self, pipeline_model_name, als_model_name, user_id):
        # Set SparkSession Object to run spark app
        self.create_spark_app()
        reviews = self.return_col(col_name="reviews")

        unwatched_books = reviews\
            .filter(F.col('reviewerID') != user_id)\
            .select("asin").distinct()

        test_data = unwatched_books.withColumn(
            "reviewerID",
            F.lit(user_id)
            )

        pipelineModel = PipelineModel.read().load(pipeline_model_name)
        transformedDf = pipelineModel.transform(test_data)
        alsModel = ALSModel.load(als_model_name)
        final_data = alsModel.transform(transformedDf)
        top_model = final_data.sort(F.desc('predict')).limit(10)
        self.spark.catalog.clearCache()
        self.spark.stop()
