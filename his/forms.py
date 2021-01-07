from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    confirm_password = PasswordField('confirm password',
                    validators =[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    # username = StringField('Username', validators =[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('password', validators =[DataRequired()])
    # confirm_password = PasswordField('confirm password',
                    # validators =[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
