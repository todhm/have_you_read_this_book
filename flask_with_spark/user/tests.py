from application import create_app as create_app_base
from settings import TEST_MONGO_URI
from mongoengine.connection import _get_db
from user.models import *
from user.form import duplicate_error
from shopping.models import Product, Review
import unittest


class UserTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(
            MONGODB_SETTINGS={
                'host': TEST_MONGO_URI
                },
            TESTING=True,
            WTF_CSRF_ENABLED=False
            )

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        self.username = "Jorge"
        self.email = "gmlaud14@gmail.com"
        self.password = "test123"

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)

    def test_duplicate_user(self):
        rv = self.app.post('/signup', data=dict(
                username=self.username,
                email=self.email,
                password=self.password,
                confirm=self.password
                ),
            follow_redirects=True
            )
        self.app.get('/logout')
        rv = self.app.post('/signup', data=dict(
                username=self.username,
                email=self.email,
                password=self.password,
                confirm=self.password
            ),
            follow_redirects=True
            )
        self.assertTrue(User.objects.filter(username=self.username).count() == 1)
        self.assertTrue(duplicate_error in rv.data.decode())

    def test_login(self):
        rv = self.app.post('/signup', data=dict(
                username=self.username,
                email=self.email,
                password=self.password,
                confirm=self.password
            ),
            follow_redirects=True
            )
        self.app.get('/logout')
        rv = self.app.post('/login', data=dict(
            email=self.email,
            password=self.password
            ))
        with self.app.session_transaction() as session:
            session['email'] == self.email

    def test_register_user(self):
        # basic registration of user
        rv = self.app.post('/signup', data=dict(
            username=self.username,
            email=self.email,
            password=self.password,
            confirm=self.password
            ),
            follow_redirects=True)
        self.assertTrue(User.objects.filter(username=self.username).count() == 1)
