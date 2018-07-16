from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError
from wtforms.fields.html5 import EmailField
from user.models import User
from shopping.models import Review
from utilities.errors import REVIEW_ERROR, COMMENT_ERROR, OVERALL_ERROR


class SearchForm(FlaskForm):
    search_query = StringField('search_query', [
        validators.DataRequired(),
        validators.Length(min=2)
        ])


class ReviewForm(FlaskForm):
    overall = FloatField('Point of the product', [
        validators.DataRequired(message=OVERALL_ERROR)
        ],
        default=0.0)
    review = TextAreaField('Comment', [
        validators.DataRequired(message=COMMENT_ERROR),
        validators.Length(min=4)
    ])

    productid = HiddenField('Productid', [
        validators.DataRequired(),
    ])

    def validate(self, email):
        if not super().validate():
            return False

        # if review already exists by same user you cannot add more
        review = Review\
            .objects\
            .filter(userid=email)\
            .filter(productid=self.productid.data)\
            .first()

        if review:
            self.review.errors.append(REVIEW_ERROR)
            return False

        return True
