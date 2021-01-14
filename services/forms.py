from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField, FileField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3
from services.models import Account

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min=2, max=20)])
    name = StringField('name', validators =[DataRequired(), Length(min=2, max=30)])
    phone = StringField('phone', validators =[DataRequired(), Length(min=2, max=14)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    confirm_password = PasswordField('confirm password',
                    validators =[DataRequired(), EqualTo('password')])
    type = RadioField('type',choices = [('patient', 'patient'), ('doctor', 'doctor')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if Account.validate_username(username.data):
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if Account.validate_email(email.data):
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    email = StringField('Email', validators =[DataRequired(), Email()])
    text = TextAreaField('We will hair From you')

    submit = SubmitField('Submit')

    def validate_email(self, email):
        if not Account.validate_email(email.data):
            raise ValidationError('This account does not exist, please register first!')

class BookAppointmentForm(FlaskForm):
    doctor = StringField('name', validators =[DataRequired(), Length(min=2, max=30)])
    time = DateTimeField('time')

    submit = SubmitField('Submit')

class scanForm(FlaskForm):
    file = FileField('upload', validators =[DataRequired()])
    submit = SubmitField('add')
