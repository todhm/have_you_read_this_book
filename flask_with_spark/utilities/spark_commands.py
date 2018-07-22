from flask import current_app as app
import os


def get_all_names():
    mongospark_package = app.config['SPARK_MONGO_PACKAGE']
    spark_command = '/spark/bin/spark-submit --packages {} '.format(mongospark_package)
    spark_command += '/app/spark/return_all_books.py '
    spark_command += app.config['SPARK_MASTER_URI'] + ' '
    spark_command += app.config["MONGODB_SETTINGS"]["host"] + ' '
    return spark_command


def return_best_books():
    mongospark_package = app.config['SPARK_MONGO_PACKAGE']
    spark_master_uri = app.config['SPARK_MASTER_URI']
    spark_command = '/spark/bin/spark-submit --packages {} '.format(mongospark_package)
    spark_command += '--master {} '.format(spark_master_uri)
    spark_command += '--deploy-mode client '
    spark_command += '/app/spark/return_best_books.py '
    spark_command += app.config['SPARK_MASTER_URI'] + ' '
    spark_command += app.config["MONGODB_SETTINGS"]["host"] + ' '
    return spark_command


def make_recommendation_model():
    mongospark_package = app.config['SPARK_MONGO_PACKAGE']
    spark_master_uri = app.config['SPARK_MASTER_URI']
    driver_memory = app.config['SPARK_DRIVER_MEMORY']
    executor_memory = app.config['SPARK_EXECUTOR_MEMORY']
    spark_command = '/spark/bin/spark-submit --packages {} '.format(mongospark_package)
    spark_command += '--master {} '.format(spark_master_uri)
    spark_command += '--deploy-mode client '
    spark_command += '--driver-memory {} '.format(driver_memory)
    spark_command += '--executor-memory {} '.format(executor_memory)
    spark_command += '/app/spark/make_recommendation_model.py '
    spark_command += app.config['SPARK_MASTER_URI'] + ' '
    spark_command += app.config["MONGODB_SETTINGS"]["host"] + ' '
    return spark_command


def make_similarity_table():
    mongospark_package = app.config['SPARK_MONGO_PACKAGE']
    spark_master_uri = app.config['SPARK_MASTER_URI']
    driver_memory = app.config['SPARK_DRIVER_MEMORY']
    executor_memory = app.config['SPARK_EXECUTOR_MEMORY']
    spark_command = '/spark/bin/spark-submit --packages {} '.format(mongospark_package)
    spark_command += '--master {} '.format(spark_master_uri)
    spark_command += '--deploy-mode client '
    spark_command += '--driver-memory {} '.format(driver_memory)
    spark_command += '--executor-memory {} '.format(executor_memory)
    spark_command += '/app/spark/make_similarity_table.py '
    spark_command += app.config['SPARK_MASTER_URI'] + ' '
    spark_command += app.config["MONGODB_SETTINGS"]["host"] + ' '
    return spark_command


def convert_to_integer():
    mongospark_package = app.config['SPARK_MONGO_PACKAGE']
    spark_master_uri = app.config['SPARK_MASTER_URI']
    driver_memory = app.config['SPARK_DRIVER_MEMORY']
    executor_memory = app.config['SPARK_EXECUTOR_MEMORY']
    spark_command = '/spark/bin/spark-submit --packages {} '.format(mongospark_package)
    spark_command += '--master {} '.format(spark_master_uri)
    spark_command += '--deploy-mode client '
    spark_command += '--driver-memory {} '.format(driver_memory)
    spark_command += '--executor-memory {} '.format(executor_memory)
    spark_command += '/app/spark/convert_to_integer.py '
    spark_command += app.config['SPARK_MASTER_URI'] + ' '
    spark_command += app.config["MONGODB_SETTINGS"]["host"] + ' '
    return spark_command


def convert_productid():
    mongospark_package = app.config['SPARK_MONGO_PACKAGE']
    spark_master_uri = app.config['SPARK_MASTER_URI']
    driver_memory = app.config['SPARK_DRIVER_MEMORY']
    executor_memory = app.config['SPARK_EXECUTOR_MEMORY']
    spark_command = '/spark/bin/spark-submit --packages {} '.format(mongospark_package)
    spark_command += '--master {} '.format(spark_master_uri)
    spark_command += '--deploy-mode client '
    spark_command += '--driver-memory {} '.format(driver_memory)
    spark_command += '--executor-memory {} '.format(executor_memory)
    spark_command += '/app/spark/convert_productid.py '
    spark_command += app.config['SPARK_MASTER_URI'] + ' '
    spark_command += app.config["MONGODB_SETTINGS"]["host"] + ' '
    return spark_command


def convert_reviewerid():
    mongospark_package = app.config['SPARK_MONGO_PACKAGE']
    spark_master_uri = app.config['SPARK_MASTER_URI']
    driver_memory = app.config['SPARK_DRIVER_MEMORY']
    executor_memory = app.config['SPARK_EXECUTOR_MEMORY']
    spark_command = '/spark/bin/spark-submit --packages {} '.format(mongospark_package)
    spark_command += '--master {} '.format(spark_master_uri)
    spark_command += '--deploy-mode client '
    spark_command += '--driver-memory {} '.format(driver_memory)
    spark_command += '--executor-memory {} '.format(executor_memory)
    spark_command += '/app/spark/convert_reviewerid.py '
    spark_command += app.config['SPARK_MASTER_URI'] + ' '
    spark_command += app.config["MONGODB_SETTINGS"]["host"] + ' '
    return spark_command
