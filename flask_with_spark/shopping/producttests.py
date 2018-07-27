from application import create_app as create_app_base
from settings import TEST_MONGO_URI
from mongoengine.connection import _get_db
import unittest
import json
from user.models import User
from shopping.models import *
from utilities.testutil import TestUtil
from utilities.errors import NO_QUERY_ERROR, NO_RESULT_FOUND
from bs4 import BeautifulSoup
from freezegun import freeze_time
from datetime import datetime as dt
from datetime import timedelta
import re


class ProductTest(TestUtil):
    def setUp(self):
        super().setUp()
        self.test_userid = "gmlaud14@gmail.com"
        self.test_user_name = "Jorge"
        rv = self.client.post('/signup', data=dict(
            username=self.test_user_name,
            email=self.test_userid,
            password="test123",
            confirm="test123"
            ),
            follow_redirects=True)
        user = User.objects.filter(email=self.test_userid).first()
        self.test_userIntId = user.userIntId

    def test_index_page_with_none(self):
        rv = self.client.get('/')
        self.assertTrue(rv.status_code == 200)

    def test_index_page_with_best_products(self):
        book_name_list = self.return_best_products(start_num=0, end_num=10)
        rv = self.client.get('/')
        page = rv.data.decode('utf-8')
        for book_name in book_name_list:
            self.assertTrue(book_name in page)

    # If similarity table prepared and user not registered any review
    def test_index_page_similarity_without_reviews(self):
        book_title_list = self.return_random_title_list(
            start_num=0,
            end_num=10,
        )
        similarity_table_list = self.return_similarity_table(
            start_num=0,
            end_num=10
            )
        rv = self.client.get('/')
        page = rv.data.decode('utf-8')
        for book_name in book_title_list:
            self.assertFalse(book_name in page)

    # If similarity table prepared and user registered reviews
    def test_index_page_similarity(self):
        book_lst, review_lst = self.return_random_product_and_reviews(
            start_num=0,
            end_num=100,
            base_book_id="",
            review_point=3,
        )
        review = "Jordan is the best player ever"
        rv = self.client.post(
            '/search_book/'+'1',
            data=dict(
                review=review,
                overall=3
                ),
            follow_redirects=True
            )
        similarity_table_list = self.return_similarity_table(
            start_num=0,
            end_num=100
            )
        rv = self.client.get('/')
        filtered_similarity_list = filter(
            lambda x: x['productid'] == '1',
            similarity_table_list
            )
        sorted_similarity = sorted(
            filtered_similarity_list,
            key=lambda x: x['similarity']
        )[:10]
        page = rv.data.decode()
        # Check review count and review overall maded properly.
        soup = BeautifulSoup(page, "html.parser")
        rating_star_list = soup.find_all("input", class_='rating-loading')
        self.assertTrue(len(rating_star_list) == 10)
        for rating_star in rating_star_list:
            self.assertTrue(int(rating_star['value']) == 3)
        review_count_list = soup.find_all("h6", class_='review-count')
        for review_count in review_count_list:
            self.assertTrue("10" in review_count.text)

        # Check product title in review list
        for similarity in sorted_similarity:
            product = Product\
                .objects\
                .filter(asin=similarity['productid'])\
                .first()
            self.assertTrue(product.title in page)

    # If similarity table is prepared for user without reviews
    def test_index_page_without_reviews_and_similarity(self):
        book_title_list = self.return_random_title_list(
            start_num=0,
            end_num=10,
        )
        rv = self.client.get('/')
        page = rv.data.decode('utf-8')
        for book_name in book_title_list:
            self.assertFalse(book_name in page)

    def test_index_page_with_best_products_morethan_20s(self):
        with freeze_time(dt.now()) as frozen_datetime:
            book_name_list = self.return_best_products(start_num=0, end_num=10)
            frozen_datetime.tick(delta=timedelta(hours=3))
            second_book_name_list = self.return_best_products(
                start_num=11,
                end_num=21
                )
        rv = self.client.get('/')
        page = rv.data.decode()
        for book_name in book_name_list:
            regular_search = book_name + '</'
            self.assertFalse(regular_search in page)

        for book_name in second_book_name_list:
            regular_search = book_name + '</'
            self.assertTrue(regular_search in page)

    # if recommendation table is prepared recommend list is on the table
    def test_index_page_with_recommendation(self):
        book_obj_lst, review_lst = self.return_random_product_and_reviews(
            start_num=0,
            end_num=10,
            base_book_id="",
            review_point=3,
            with_int_id=True,
        )
        book_id_lst = [book['productIntId'] for book in book_obj_lst]
        similarity_table_list = self.add_recommendation_table(
            userid=self.test_userIntId,
            product_list=book_id_lst,
        )
        rv = self.client.get('/')
        page = rv.data.decode('utf-8')

        # Check review count and review overall maded properly.
        soup = BeautifulSoup(page, "html.parser")
        rating_star_list = soup.find_all("input", class_='rating-loading')
        self.assertTrue(len(rating_star_list) == 10)
        for rating_star in rating_star_list:
            self.assertTrue(int(rating_star['value']) == 3)
        review_count_list = soup.find_all("h6", class_='review-count')
        for review_count in review_count_list:
            self.assertTrue("10" in review_count.text)
        for book_obj in book_obj_lst:
            self.assertTrue(book_obj['title'] in page)

    # if made recommendation many time get latest recommendation
    def test_index_page_with_latest_recommendation(self):
        with freeze_time(dt.now()) as frozen_datetime:
            first_book_obj_list = self.return_added_book_lst(
                start_num=0,
                end_num=10,
                title="firsttest"
            )
            first_book_id_lst = [book['productIntId'] for book in first_book_obj_list]
            similarity_table_list = self.add_recommendation_table(
                userid=self.test_userIntId,
                product_list=first_book_id_lst
            )
            frozen_datetime.tick(delta=timedelta(seconds=1))
            second_book_obj_list = self.return_added_book_lst(
                start_num=10,
                end_num=20,
                title="secondtest"
            )
            second_book_id_lst = [book['productIntId'] for book in second_book_obj_list]
            similarity_table_list = self.add_recommendation_table(
                userid=self.test_userIntId,
                product_list=second_book_id_lst,
            )
        rv = self.client.get('/')
        page = rv.data.decode('utf-8')
        for book_obj in first_book_obj_list:
            self.assertFalse(book_obj['title'] in page)

        for book_obj in second_book_obj_list:
            self.assertTrue(book_obj['title'] in page)

    def test_get_book_names(self):
        sentence_lst = [
            "yellow world", "bye bye world",
            "hello world", "askdjf;alskdadfadsf", 'hello'
            ]

        for sentence in sentence_lst:
            productName = ProductName(title=sentence)
            productName.save()

        rv = self.client.get('/book_names/'+"hello")
        sorted_lst = json.loads(rv.data.decode())
        assert(sorted_lst[0] == "hello")
        assert(sorted_lst[1] == "hello world")

    def test_get_book_name_unquote(self):
        sentence_lst = [
            "yellow world", "hello world",
            "hellow world", "world hello", 'hello'
            ]

        for sentence in sentence_lst:
            productName = ProductName(title=sentence)
            productName.save()

        rv = self.client.get('/book_names/'+"hello world")
        sorted_lst = json.loads(rv.data.decode())
        assert(sorted_lst[0] == "hello world")

    def test_product_search(self):
        title_list = self.return_random_title_list(
            start_num=0,
            end_num=10,
            title="test_title"
            )
        rv = self.client.post(
            '/search_book_lst',
            data=dict(
                search_query="test_title"
            ),
            follow_redirects=True
        )
        page = rv.data.decode()
        for title in title_list:
            self.assertTrue(title in page)

    def test_product_search_with_invalid_results(self):
        title_list = self.return_random_title_list(
            start_num=0,
            end_num=10,
            title="test_title"
            )
        rv = self.client.post(
            '/search_book_lst',
            data=dict(
                search_query="brazil"
            ),
            follow_redirects=True
        )
        page = rv.data.decode()
        self.assertTrue(NO_RESULT_FOUND in page)

    def test_product_search_with_none_query(self):
        title_list = self.return_random_title_list(
            start_num=0,
            end_num=10
            )
        rv = self.client.post(
            '/search_book_lst',
            data=dict(
                search_query=""
            ),
            follow_redirects=True
        )
        page = rv.data.decode()
        self.assertTrue(NO_QUERY_ERROR in page)
