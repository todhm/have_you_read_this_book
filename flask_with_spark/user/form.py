import bcrypt
from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.validators import ValidationError
from wtforms.fields.html5 import EmailField
from user.models import User


duplicate_error = "Email is already in use"


class SignUpForm(FlaskForm):
    email = EmailField('Email address', [
        validators.DataRequired(),
        validators.Email()
        ])
    username = StringField('Username', [
            validators.DataRequired(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')

    def validate_email(form, field):
        if User.objects.filter(email=field.data).first():
            raise ValidationError(duplicate_error)


class LoginForm(FlaskForm):
    email = StringField('Email', [
            validators.DataRequired(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('Password', [
            validators.DataRequired(),
            validators.Length(min=4, max=80)
        ])

    def validate_email(form, field):
        user = User.objects.filter(email=field.data).first()
        if not user:
            raise ValidationError("Email does not exists")
        if bcrypt.hashpw(form.password.data.encode(), user.password.encode())!= user.password.encode():
            raise ValidationError("Invalid Password")
