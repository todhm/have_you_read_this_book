import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from spark.sparkapp import SparkApp


if __name__ == "__main__":
    master_uri = sys.argv[1]
    mongo_uri = sys.argv[2]
    pipeline_model_name = sys.argv[3]
    recommendation_model_name = sys.argv[4]
    user_id = sys.argv[5]
    sa = SparkApp(master_uri=master_uri, mongo_uri=mongo_uri)
    sa.load_model(pipeline_model_name, recommendation_model_name, user_id)
