import os
import sys
import unittest
from user.tests import UserTest
from shopping.reviewtests import ReviewTest
from shopping.producttests import ProductTest
from spark.tests import SparkAppTest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


if __name__ == "__main__":
    unittest.main()
