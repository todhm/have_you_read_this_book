from mongoengine import CASCADE
from application import db
from utilities.common import utc_now_ts as now
from user.models import User


class Product(db.DynamicDocument):
    meta = {
        'collection': 'products',
        'shard_key': 'asin',
        'indexes': [
            'title',
            "asin",
            '-created',
            {"fields": ['$title', '$description'],
             "default_language":'english',
             'weights':{'title': 7, 'description': 3}}
             ]
    }
    asin = db.StringField(db_field="asin", required=True, unique=True)
    title = db.StringField(db_field="title", required=True)
    description = db.StringField(db_field="description", required=True)
    imageUrl = db.StringField(db_field="imUrl")
    created = db.IntField(db_filed="c", default=now())
    related = db.DictField(db_filed="related")
    price = db.FloatField(db_filed="price")


class Review(db.DynamicDocument):
    meta = {
        'collection': 'reviews',
        'indexes': ['asin', 'reviewerID', '-unixReviewTime'],
        'shard_key': ('asin', 'reviewerID'),
    }
    userid = db.StringField(db_field="reviewerID", required=True)
    productid = db.StringField(db_field="asin", required=True)
    username = db.StringField(db_field="reviewerName")
    helpful = db.ListField(db_field="helpful")
    created = db.IntField(db_field="unixReviewTime", default=now())
    review = db.StringField(db_field="reviewText")
    overall = db.FloatField(db_field="overall")
    title = db.StringField(db_fiedl="summary")


class ProductName(db.DynamicDocument):
    meta = {
        'collection': 'product_name',
        'indexes': [
            'title',
            {"fields": ['$title'],
             "default_language":'english',
             }
        ],
        'shard_key': 'title',
    }
    title = db.StringField(db_field="title", required=True)


class BestProduct(db.DynamicDocument):
    meta = {
        'collection': 'best_product',
        'indexes': ['t']
    }
    asin = db.StringField(db_field="asin", required=True)
    avgOverall = db.FloatField(db_field="ao")
    title = db.StringField(db_field="t", required=True)
    price = db.FloatField(db_filed="p")
    imageUrl = db.StringField(db_field="iu")
    description = db.StringField(db_field="d")
    cnt = db.IntField(db_field="cnt")
    created = db.IntField(db_filed="dc", default=now())


class RecommendTable(db.DynamicDocument):
    meta = {
        'collection': 'recommendation_table',
        'indexes': ['t']
    }
    userid = db.StringField(db_field="reviewerID")
    recommendList = db.ListField(db_field="recommendations", required=True)
    created = db.IntField(db_filed="dc", default=now())


class SimilarityTable(db.DynamicDocument):
    meta = {
        'collection': 'similarity_table',
        'indexes': ['item'],
        'shard_key': 'productid',
    }
    productid = db.StringField(db_field="item", required=True)
    product_match = db.StringField(db_field="item_other")
    similarity = db.FloatField(db_field="sim", required=True)
