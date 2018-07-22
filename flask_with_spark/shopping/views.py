import random
import string
import httplib2
import json
import requests
from flask import *
from application import mongo
from utilities.decorators import login_required
from utilities.errors import *
from user.form import SignUpForm, LoginForm
from user.models import User
from shopping.models import *
from shopping.form import ReviewForm, SearchForm
from mongoengine.queryset.visitor import Q
from urllib.parse import unquote

shopping_app = Blueprint('shopping_app', __name__, template_folder='templates')


@shopping_app.route('/')
@login_required
def homepage():
    form = SearchForm()
    error = None
    # Get best product based on review
    best_product_list = BestProduct.objects.order_by("-created").limit(10)
    userIntId = session['userIntId']
    email = session['email']
    # Show the most similar books based on last user review
    if Review.objects.filter(userid=session['email']).count() > 0:
        last_review = Review\
            .objects\
            .filter(userid=session['email'])\
            .order_by('-created')\
            .first()
        last_product = Product\
            .objects\
            .filter(asin=last_review.productid)\
            .first()
        similarity_list = SimilarityTable\
            .objects\
            .filter(productid=last_review.productid)\
            .order_by('-similarity')\
            .limit(10)
        product_id_list = [similarity.product_match
                           for similarity in similarity_list]
        similar_products = Product\
            .objects\
            .filter(asin__in=product_id_list)
    else:
        last_product = None
        similar_products = None

    if RecommendTable.objects.filter(userIntId=userIntId).count() > 0:
        last_recommend = RecommendTable\
            .objects\
            .filter(userIntId=session['userIntId'])\
            .order_by("-created")\
            .first()
        product_lst = last_recommend.recommendList
        product_id_lst = [product['pI'] for product in product_lst]
        recommend_products = Product\
            .objects\
            .filter(productIntId__in=product_id_lst)
    else:
        recommend_products = None
    return render_template(
        "shoppings/index.html",
        best_product_list=best_product_list,
        similar_products=similar_products,
        last_product=last_product,
        form=form,
        error=error,
        recommend_products=recommend_products
    )


@shopping_app.route('/book_names/<string:book_name>')
@login_required
def get_book_names(book_name=""):
    if book_name:
        book_name = unquote(book_name)
        product_name_list = ProductName\
            .objects\
            .search_text(book_name)\
            .order_by('$text_score')\
            .limit(10)
        name_list = [product_name.title for product_name in product_name_list]
        return jsonify(name_list)
    else:
        return jsonify([])


@shopping_app.route('/search_book_lst', methods=["POST"])
@login_required
def search_book_lst():
    form = SearchForm()
    if not form.validate():
        flash(NO_QUERY_ERROR)
        return redirect(url_for('shopping_app.homepage'))
    return redirect(
        url_for(
            'shopping_app.get_book_lst',
            search_query=form.search_query.data
             ))


@shopping_app.route('/book_lst/<string:search_query>/<int:page>')
@shopping_app.route('/book_lst/<string:search_query>/', defaults={'page': 1})
@login_required
def get_book_lst(search_query="", page=1):
    form = SearchForm()
    per_page = current_app.config['PER_PAGE']
    search_query = unquote(search_query)
    # Get Products which have closest result with query
    products = Product\
        .objects\
        .search_text(search_query)\
        .order_by('$text_score')\
        .paginate(page=page, per_page=per_page)

    return render_template("shoppings/search_result.html", products=products,
                           form=form, search_query=search_query,
                           error=NO_RESULT_FOUND)


@shopping_app.route('/search_book/<string:find_value>',
                    methods=["GET", "POST"], defaults={'page': 1})
@shopping_app.route('/search_book/<string:find_value>/<int:page>',
                    methods=["GET", "POST"])
@login_required
def find_book(find_value="", page=1):
    # Get book by their book id or title
    find_value = unquote(find_value)
    book = Product.objects.filter(
        Q(__raw__={'asin': find_value}) |
        Q(__raw__={'title': find_value})).first()

    if not book:
        abort(404)

    # Get Reviews of the book
    form = ReviewForm(productid=book.asin)
    per_page = current_app.config['PER_PAGE']
    reviews = Review\
        .objects\
        .filter(productid=book.asin)\
        .order_by("-created")\
        .paginate(page=page, per_page=per_page)
    # If user add  validated review on new page add review and show it
    if request.method == "POST" and form.validate(email=session['email']):
        productIntId = book.productIntId
        review = Review(
            userid=session['email'],
            productid=form.productid.data,
            username=session['username'],
            review=form.review.data,
            overall=form.overall.data,
            reviewerIntId=session['userIntId'],
            productIntId=productIntId,
        )
        review.save()
        return redirect(
            url_for(
                'shopping_app.find_book',
                find_value=find_value,
                page=page
                ))

    return render_template("shoppings/product.html", book=book,
                           reviews=reviews, form=form)


@shopping_app.route('/add_review', methods=["POST"])
@login_required
def add_review():
    # Get book by their book id or title
    find_value = unquote(find_value)
    pass
