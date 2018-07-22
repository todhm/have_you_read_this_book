import os
from flask import current_app as app
from application import celery
from spark.sparkapp import SparkApp
from utilities.spark_commands import *


@celery.task(bind=True)
def get_all_names_task(self):
    spark_command = get_all_names()
    os.system(spark_command)


@celery.task(bind=True)
def return_best_books_task(self):
    spark_command = return_best_books()
    os.system(spark_command)


@celery.task(bind=True)
def make_similarity_table_task(self):
    spark_command = make_similarity_table()
    os.system(spark_command)


@celery.task(bind=True)
def make_recommendation_task(self):
    spark_command = make_recommendation_model()
    os.system(spark_command)


@celery.task(bind=True)
def convert_to_integer_task(self):
    spark_command = convert_to_integer()
    os.system(spark_command)
