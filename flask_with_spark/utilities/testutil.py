import os
from flask import app
from random import randint, uniform
from application import create_app
from settings import TEST_MONGO_URI
from shopping.models import *
from pymongo import MongoClient
from mongoengine.connection import _get_db
import unittest
from utilities.common import utc_now_ts
import time


class TestUtil(unittest.TestCase):
    def create_app(self):
        app = create_app(
                MONGODB_SETTINGS={
                    'host': TEST_MONGO_URI,
                    },
                MONGO_URI=TEST_MONGO_URI,
                TESTING=True,
                WTF_CSRF_ENABLED=False
            )
        return app

    def setUp(self):
        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        self._started_at = time.time()

    def tearDown(self):
        elapsed = time.time() - self._started_at
        print('{} ({}s)'.format(self.id(), round(elapsed, 2)))
        db = _get_db()
        db.client.drop_database(db)
        db.client.close()
        self.app_context.pop()

    def return_random_title_list(self, start_num=0, end_num=100,
                                 title="test", description="test_description"):
        title_list = []
        product_list = []
        Product.ensure_indexes()
        for i in range(start_num, end_num):
            book_id = str(i)
            book_name = title + ' ' + book_id
            book_description = description + ' ' + book_id
            product = Product(
                asin=book_id,
                title=book_name,
                description=book_description,
                )
            product_list.append(product)
            title_list.append(book_name)

        Product.objects.insert(product_list)
        return title_list

    def return_added_book_lst(self, start_num=0, end_num=100,
                              title="test", description="test_description"):
        book_obj_list = []
        product_list = []
        Product.ensure_indexes()
        for i in range(start_num, end_num):
            book_id = str(i)
            book_name = title + book_id
            book_description = description + book_id
            book_obj = dict(
                asin=book_id,
                productIntId=i,
                title=book_name,
                description=book_description
            )
            product = Product(
                asin=book_id,
                productIntId=i,
                title=book_name,
                description=book_description,
                )
            product_list.append(product)
            book_obj_list.append(book_obj)
        Product.objects.insert(product_list)
        return book_obj_list

    def return_random_user(self, user_start_num=0, user_end_num=100,
                           base_id="todhm", base_email="@gmail.com"):
        user_list = []
        for i in range(user_start_num, user_end_num):
            email = base_id + str(i) + base_email
            user = User(
                username=str(i),
                password='test1234',
                email=email,
                userIntId=i,
            )
            user_list.append(user)
        User.objects.insert(user_list)

    def return_random_review_list(self, product_id, start_num=0, end_num=100,
                                  review_description="test", review_point=None,
                                  base_id="todhm", base_email="@gmail.com",
                                  created=None):
        review_obj_list = []
        review_list = []
        Review.ensure_indexes()
        for i in range(start_num, end_num):
            test_user_id = base_id + str(i) + base_email
            test_user_name = "test_user_name" + str(i)
            test_review_description = review_description + str(i)
            overall = randint(0, 5) if review_point is None \
                else review_point
            created = created if created else utc_now_ts()
            review_obj = dict(
                userid=test_user_id,
                productid=product_id,
                username=test_user_name,
                review=test_review_description,
                overall=overall,
                created=created,
            )
            review = Review(
                userid=test_user_id,
                productid=product_id,
                username=test_user_name,
                review=test_review_description,
                overall=overall,
                created=created,
                )
            review_obj_list.append(review_obj)
            review_list.append(review)
        Review.objects.insert(review_list)
        return review_obj_list

    def return_random_title_and_reviews(self,
                                        start_num=0, end_num=100,
                                        reviewer_start_num=0,
                                        reviewer_end_num=10,
                                        review_point=None,
                                        base_id="todhm",
                                        base_email="@gmail.com",
                                        base_bookname="test",
                                        base_description="test_description"

                                        ):
        asin_list = []
        product_list = []
        review_list = []
        Review.ensure_indexes()
        Product.ensure_indexes()
        for i in range(start_num, end_num):
            book_id = str(i)
            book_name = base_bookname + book_id
            description = base_description + book_id
            product = Product(
                asin=book_id,
                productIntId=i,
                title=book_name,
                description=description,
                price=randint(100, 100000),
                imageUrl=description,
                )
            product_list.append(product)
            asin_list.append(book_id)

            for x in range(reviewer_start_num, reviewer_end_num):
                test_user_id = base_id + str(x) + base_email
                overall = randint(0, 5) if review_point is None\
                    else review_point
                review = Review(
                    productIntId=i,
                    reviewerIntId=x,
                    userid=test_user_id,
                    productid=book_id,
                    username="test",
                    review="good",
                    overall=overall
                )
                review_list.append(review)

        Product.objects.insert(product_list)
        Review.objects.insert(review_list)
        return asin_list

    def return_random_product_and_reviews(self,
                                          start_num=0, end_num=100,
                                          reviewer_start_num=0,
                                          reviewer_end_num=10,
                                          review_point=None,
                                          base_book_id="testid",
                                          base_id="todhm",
                                          base_email="@gmail.com",
                                          base_bookname="test",
                                          base_description="test_description",
                                          imageUrl="/src/test/test",
                                          with_int_id=False,
                                          ):
        product_list = []
        return_product_list = []
        review_list = []
        return_review_list = []
        Review.ensure_indexes()
        Product.ensure_indexes()
        for i in range(start_num, end_num):
            book_id = base_book_id + str(i)
            book_name = base_bookname + book_id
            description = base_description + book_id
            price = randint(100, 100000)
            if with_int_id:
                product_obj = dict(
                    asin=book_id,
                    productIntId=i,
                    title=book_name,
                    description=description,
                    price=price,
                    imageUrl=imageUrl,
                )
                product = Product(
                    asin=book_id,
                    productIntId=i,
                    title=book_name,
                    description=description,
                    price=price,
                    imageUrl=imageUrl,
                    )
            else:
                product_obj = dict(
                    asin=book_id,
                    title=book_name,
                    description=description,
                    price=price,
                    imageUrl=imageUrl,
                )
                product = Product(
                    asin=book_id,
                    title=book_name,
                    description=description,
                    price=price,
                    imageUrl=imageUrl,
                    )
            return_product_list.append(product_obj)
            product_list.append(product)

            for x in range(reviewer_start_num, reviewer_end_num):
                test_user_id = base_id + str(x) + base_email
                overall = randint(0, 5) if review_point is None\
                    else review_point

                if with_int_id:
                    review = Review(
                        userid=test_user_id,
                        reviewerIntId=x,
                        productIntId=i,
                        productid=book_id,
                        username="test",
                        review="good",
                        overall=overall
                    )
                    review_obj = dict(
                        userid=test_user_id,
                        reviewerIntId=x,
                        productIntId=i,
                        productid=book_id,
                        username="test",
                        review="good",
                        overall=overall
                    )

                else:
                    review = Review(
                        userid=test_user_id,
                        productid=book_id,
                        username="test",
                        review="good",
                        overall=overall
                    )
                    review_obj = dict(
                        userid=test_user_id,
                        productid=book_id,
                        username="test",
                        review="good",
                        overall=overall
                    )
                return_review_list.append(review_obj)
                review_list.append(review)

        Product.objects.insert(product_list)
        Review.objects.insert(review_list)
        return return_product_list, return_review_list

    def add_multiple_review_for_user(self, reviewer_id, start_num=0,
                                     end_num=100, username="test",
                                     review_comment="good", review_point=None):
        asin_list = []
        review_list = []
        Review.ensure_indexes()
        for i in range(start_num, end_num):
            book_id = str(i)
            overall = randint(0, 5) if review_point is None\
                else review_point
            review = Review(
                userid=reviewer_id,
                productid=book_id,
                username=username,
                review=review_comment,
                overall=overall
            )
            review_list.append(review)
        Review.objects.insert(review_list)
        return asin_list

    def return_best_products(self, start_num=0, end_num=100,
                             reviewOverall=5, cnt=100):
            book_name_list = []
            best_product_list = []
            now_time = utc_now_ts()
            for i in range(start_num, end_num):
                book_id = str(i)
                book_name = "test" + book_id
                description = "test_description" + book_id
                bestProduct = BestProduct(
                    asin=book_id,
                    title=book_name,
                    avgOverall=reviewOverall,
                    description=description,
                    cnt=cnt,
                    imageUrl=description,
                    created=now_time
                )

                best_product_list.append(bestProduct)
                book_name_list.append(book_name)
            BestProduct.objects.insert(best_product_list)
            return book_name_list

    def return_similarity_table(self, start_num=0, end_num=100):
        similarity_list = []
        similarity_table_list = []
        now_time = utc_now_ts()
        for x in range(start_num, end_num):
            for y in range(start_num, end_num):
                if x != y:
                    similarity_point = uniform(0, 1)
                    similarity_dict = dict(
                        productid=str(x),
                        product_match=str(y),
                        similarity=similarity_point
                    )
                    similarity = SimilarityTable(
                        productid=str(x),
                        product_match=str(y),
                        similarity=similarity_point
                    )
                    similarity_table_list.append(similarity)
                    similarity_list.append(similarity_dict)
        SimilarityTable.objects.insert(similarity_table_list)
        return similarity_list

    def add_recommendation_table(self, userid, product_list):
        product_list = [
            {"pI": product_id, "rating": randint(0, 5)}
            for product_id in product_list
            ]
        created = utc_now_ts()
        recommendTable = RecommendTable(
            userIntId=userid,
            recommendList=product_list,
            created=created
        )
        recommendTable.save()
        return recommendTable
