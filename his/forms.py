from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import mysql.connector
from his.routes import mydb

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min=2, max=20)])
    name = StringField('name', validators =[DataRequired(), Length(min=2, max=30)])
    phone = StringField('phone', validators =[DataRequired(), Length(min=2, max=14)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    confirm_password = PasswordField('confirm password',
                    validators =[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        # get a similar field in mydb
        cur = mydb.cursor()
        cur.execute("SELECT username FROM Accounts WHERE username = %s", (username, ))
        result = cur.fetchall()
        cur.close()

        if result:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):

        # get a similar field in mydb
        cur = mydb.cursor()
        cur.execute("SELECT email FROM Accounts WHERE email = %s", (email, ))
        result = cur.fetchall()
        cur.close()

        if result:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    # username = StringField('Username', validators =[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    # confirm_password = PasswordField('confirm password',
                    # validators =[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
