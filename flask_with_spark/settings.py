import os
import json
from datetime import datetime


TEST_MONGO_URI = 'mongodb://mongos1/test_shoppings'


class BaseConfig:
    """Base	configuration"""
    TESTING = False
    SECRET_KEY = b'U\xb9\x8e\x1f\xc1\xe3p|l\x90\xe2\xf7\xb2\x14\xcb\x95\xd1,\x12\x1a\xef\x01mH'
    DEBUG = True

    # CelerySetting
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Europe/Oslo'
    enable_utc = True

    # Spark settings
    SPARK_MASTER_URI = "spark://spark-master:7077"
    SPARK_MONGO_PACKAGE = "org.mongodb.spark:mongo-spark-connector_2.11:2.2.3"
    UPLOADED_SPARK_URL = 'file:/workspace/flask_spark/static/spark_model/'

    # PAGE settings
    PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    MONGODB_SETTINGS = {
            'host': 'mongodb://mongos1/sample_shoppings'
        }
    # MONGO_URIS
    MONGO_URI = 'mongodb://mongos1/sample_shoppings'


class ProductionConfig(BaseConfig):
    MONGODB_SETTINGS = {
            'host': 'mongodb://mongos1/shoppings'
        }
    # MONGO_URIS
    MONGO_URI = 'mongodb://mongos1/shoppings'
