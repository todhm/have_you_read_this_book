from utilities.testutil import TestUtil
from utilities.spark_commands import *
from utilities.common import utc_now_ts as now
from shopping.models import *
from spark.sparkapp import SparkApp
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql import Row
from pyspark.sql import functions as F
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml import PipelineModel
from pymongo import MongoClient
from mongoengine.connection import _get_db
import os


class SparkAppTest(TestUtil):

    def test_Names(self):
        title_list = self.return_random_title_list()
        mongospark_package = self.app.config['SPARK_MONGO_PACKAGE']
        spark_command = get_all_names()
        os.system(spark_command)
        product_names = ProductName.objects.order_by("title")
        product_name_list = sorted([pn.title for pn in product_names])
        title_list = sorted(title_list)
        self.assertTrue(len(product_name_list) == len(title_list))
        for idx, title in enumerate(product_name_list):
            self.assertTrue(title == title_list[idx])

    def test_write_duplicate_names(self):
        title_list = self.return_random_title_list()
        spark_command = get_all_names()
        os.system(spark_command)
        os.system(spark_command)
        product_names = ProductName.objects.order_by("title")
        product_name_list = sorted([pn.title for pn in product_names])
        title_list = sorted(title_list)
        self.assertTrue(len(product_name_list) == len(title_list))
        for idx, title in enumerate(product_name_list):
            self.assertTrue(title == title_list[idx])

    # get products with less than 10 reviews
    def test_get_best_app_with_smaller_reviews(self):
        title_list = self.return_random_title_and_reviews(
            reviewer_start_num=0,
            reviewer_end_num=4
            )
        spark_command = return_best_books()
        os.system(spark_command)
        bestProductList = BestProduct.objects.order_by("-created")
        self.assertTrue(len(bestProductList) == 0)

    # get product with more than 10 reviews of less than 10 products
    def test_get_best_app_with_smaller_products(self):
        title_list = self.return_random_title_and_reviews(
            start_num=0,
            end_num=7,
            reviewer_start_num=0,
            reviewer_end_num=10,
            review_point=5,
            )
        spark_command = return_best_books()
        os.system(spark_command)
        bestProductList = BestProduct.objects
        self.assertTrue(len(bestProductList) == 7)
        for bestProduct in bestProductList:
            self.assertTrue(bestProduct.avgOverall == 5)
            self.assertTrue(bestProduct.cnt == 10)

    # get product with more than 10 reviews of more than 10 products
    def test_get_best_app(self):
        title_list = self.return_random_title_and_reviews(
            start_num=0,
            end_num=10,
            reviewer_start_num=0,
            reviewer_end_num=10,
            review_point=5,
            )
        title_list = self.return_random_title_and_reviews(
            start_num=11,
            end_num=20,
            reviewer_start_num=0,
            reviewer_end_num=10,
            review_point=3,
            )
        spark_command = return_best_books()
        os.system(spark_command)
        bestProductList = BestProduct.objects
        self.assertTrue(len(bestProductList) == 10)
        for bestProduct in bestProductList:
            self.assertTrue(bestProduct.avgOverall == 5)
            self.assertTrue(bestProduct.cnt == 10)

    def test_make_recommendation(self):
        self.return_random_user(user_start_num=0, user_end_num=10)
        title_list = self.return_random_title_and_reviews(
            start_num=0,
            end_num=200,
            reviewer_start_num=0,
            reviewer_end_num=10,
        )
        spark_command = make_recommendation_model()
        os.system(spark_command)
        recommendTableList = RecommendTable.objects
        self.assertTrue(len(recommendTableList) == 10)
        for recommend in recommendTableList:
            self.assertTrue(type(recommend.userid) == str)
            self.assertTrue(len(recommend.recommendList) == 10)

    def test_make_similarity_table(self):
        title_list = self.return_random_title_and_reviews(
            start_num=0,
            end_num=200,
            reviewer_start_num=0,
            reviewer_end_num=10,
            )

        spark_command = make_similarity_table()
        os.system(spark_command)
        similarityList = SimilarityTable.objects
        for similarity in similarityList:
            self.assertTrue(type(similarity.similarity) == float)
            self.assertTrue(type(similarity.productid) == str)
            self.assertTrue(type(similarity.product_match) == str)
        self.assertTrue(len(similarityList) == (200*199))
