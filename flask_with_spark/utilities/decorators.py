from functools import wraps
from flask import session,request,redirect,url_for, abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get('email') is None:
            return redirect(url_for('user_app.login',next=request.url))
        return f(*args,**kwargs)
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get('email') :
            return redirect(url_for('shopping_app.homepage',next=request.url))
        return f(*args,**kwargs)
    return decorated_function
