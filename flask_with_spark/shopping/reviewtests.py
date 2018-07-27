from application import create_app as create_app_base
from settings import TEST_MONGO_URI
from mongoengine.connection import _get_db
import unittest
import json
from user.models import User
from shopping.models import *
from utilities.testutil import TestUtil
from utilities.errors import *
from freezegun import freeze_time
from datetime import datetime as dt, timedelta
import time

class ReviewTest(TestUtil):

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
        self.test_bookid = "122220101001"
        self.test_product_title = "selfproducttitle"
        self.test_description = "test description"
        product = Product(
            asin=self.test_bookid,
            title=self.test_product_title,
            description=self.test_description,
            )
        product.save()

    def test_get_book_page_without_review(self):
        rv = self.client.get('/search_book/'+self.test_bookid)
        page = rv.data.decode()
        self.assertTrue(self.test_bookid in page)
        self.assertTrue(self.test_product_title in page)
        self.assertTrue(self.test_description in page)

    def test_get_page_with_reviews(self):
        review_list = self.return_random_review_list(
            product_id=self.test_bookid,
            start_num=0,
            end_num=10
            )
        rv = self.client.get('/search_book/'+self.test_bookid)
        page = rv.data.decode()
        for review in review_list:
            self.assertTrue(review['productid'] in page)
            self.assertTrue(review['review'] in page)

    def test_get_page_with_reviews_and_pagination(self):
        with freeze_time(dt.now()) as frozen_datetime:
            first_review_list = self.return_random_review_list(
                product_id=self.test_bookid,
                start_num=0,
                end_num=10,
                review_description="hello"
                )
            frozen_datetime.tick(delta=timedelta(seconds=1))
            second_review_list = self.return_random_review_list(
                product_id=self.test_bookid,
                start_num=10,
                end_num=20,
                review_description="yellow"
                )

        # Only old reviews are seen in sencond page
        rv = self.client.get('/search_book/' + self.test_bookid + '/2')
        page = rv.data.decode()
        for review in first_review_list:
            self.assertTrue(review['productid'] in page)
            self.assertTrue(review['review'] in page)
        for review in second_review_list:
            self.assertFalse(review['review'] in page)


    def test_add_review(self):
        review_txt = "Jordan is the best player ever"
        rv = self.client.post(
            '/search_book/'+self.test_bookid,
            data=dict(
                review=review_txt,
                overall=3
                ),
            follow_redirects=True
            )

        # show data added successfully
        review = Review.objects.first()
        self.assertTrue(review.review == review_txt)

        # show newly added review in next page
        page = rv.data.decode()
        self.assertTrue(review_txt in page)

    def test_add_imporoper_reviews(self):
        rv = self.client.post(
            '/search_book/'+self.test_bookid,
            data=dict(
                overall=3
                ),
            follow_redirects=True
            )
        page = rv.data.decode()
        self.assertTrue(COMMENT_ERROR in page)
        rv = self.client.post(
            '/search_book/'+self.test_bookid,
            data=dict(
                review="test"
                ),
            follow_redirects=True
            )
        page = rv.data.decode()
        self.assertTrue(OVERALL_ERROR in page)

    def test_add_duplicate_reviews(self):
        review = "Jordan is the best player ever"
        rv = self.client.post(
            '/search_book/'+self.test_bookid,
            data=dict(
                review=review,
                overall=3
                ),
            follow_redirects=True
            )
        new_review = "Jordan is the best player ever!@#!#"
        rv = self.client.post(
            '/search_book/'+self.test_bookid,
            data=dict(
                review=new_review,
                overall=3
                ),
            follow_redirects=True
            )
        page = rv.data.decode()
        self.assertTrue(REVIEW_ERROR in page)
