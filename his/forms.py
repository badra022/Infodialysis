from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min=2, max=20)])
    name = StringField('name', validators =[DataRequired(), Length(min=2, max=30)])
    phone = StringField('phone', validators =[DataRequired(), Length(min=2, max=14)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    confirm_password = PasswordField('confirm password',
                    validators =[DataRequired(), EqualTo('password')])
    doctor = BooleanField('I am doctor')
    patient = BooleanField('I am patient')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        # get a similar field in mydb
        # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT username FROM patient_account WHERE username = ?''', (username.data, ))
        data = False # reference the variable because of the unique accounts cannot reduce validationError
        try:
            data = cur.fetchone()[0]
        except:
            pass
        if data:
            raise ValidationError('That username is taken. Please choose a different one.')

        cur.execute('''SELECT username FROM doctor_account WHERE username = ?''', (username.data, ))
        try:
            data = cur.fetchone()[0]
        except:
            pass
        if data:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):

        # get a similar field in mydb
        # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT email FROM patient_account WHERE email = ?''', (email.data, ))
        data = False # reference the variable because of the unique accounts cannot reduce validationError
        try:
            data = cur.fetchone()[0]
        except:
            pass

        if data:
            raise ValidationError('That email is taken. Please choose a different one.')

        cur.execute('''SELECT email FROM doctor_account WHERE email = ?''', (email.data, ))
        try:
            data = cur.fetchone()[0]
        except:
            pass

        if data:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    # username = StringField('Username', validators =[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    # confirm_password = PasswordField('confirm password',
                    # validators =[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
