from flask_wtf import FlaskForm
from myproject.models import User
from wtforms import StringField, PasswordField, SubmitField, RadioField , TextAreaField , DateTimeField
from wtforms.validators import DataRequired,Email,EqualTo , Length
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()] )
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()] )
    phone = StringField('Phone Number', validators=[DataRequired()])
    job = RadioField(u'', choices=[('patient', 'I am a patient'), ('doctor', 'i am a Doctor')] , validators=[DataRequired()])
    submit = SubmitField('Register!')


        # Check if not None for that user email!
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email has been registered')


        # Check if not None for that username!
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username has been registered')

class ContactForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(),Email()])
    text = TextAreaField( 'Your message', validators=[DataRequired()])
    submit = SubmitField('Submit!')


class BookAppointment(FlaskForm):
    doctor = StringField('name', validators =[DataRequired()])
    name = StringField('name', validators =[DataRequired()])
    time = DateTimeField('time')

    submit = SubmitField('Submit')
