import random
import bcrypt
import string
import httplib2
import json
import requests
from utilities.decorators import login_required,logout_required
from user.form import SignUpForm, LoginForm
from user.models import User
from flask import Blueprint, render_template,session,make_response,request,flash,jsonify,redirect,url_for
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from application import celery

user_app = Blueprint('user_app',__name__,template_folder='templates')

@user_app.route('/login',methods=('GET', 'POST'))
@logout_required
def login():
    form = LoginForm()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    if request.method== "GET" and request.args.get("next"):
        session['next'] = request.args.get('next')
    if form.validate_on_submit():
        user = User.objects.filter(email = form.email.data).first()
        session['username'] = user.username
        session['email'] = user.email
        if 'next' in session:
            next = session.get('next')
            session.pop('next')
            return redirect(next)
        else:
            return redirect(url_for('shopping_app.homepage'))
    return render_template("user/login.html",form=form,STATE=state)

@user_app.route('/signup',methods=('GET', 'POST'))
@logout_required
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data.encode(),salt)
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data
            )
        user.save()
        session['username'] = form.username.data
        session['email']  = form.email.data
        return redirect(url_for("shopping_app.homepage"))

    return render_template("user/signup.html",form=form)


@user_app.route('/logout')
def logout():
    session.pop('email')
    session.pop('username')
    return redirect(url_for('user_app.login'))
