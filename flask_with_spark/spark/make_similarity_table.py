import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from spark.sparkapp import SparkApp


if __name__ == "__main__":
    master_uri = sys.argv[1]
    mongo_uri = sys.argv[2]
    sa = SparkApp(master_uri=master_uri, mongo_uri=mongo_uri)
    sa.make_similarity_table()
