from flask_wtf import FlaskForm
from myproject.models import User , Appointment
from wtforms import StringField, PasswordField, SubmitField, RadioField , TextAreaField ,FileField , SelectField
from wtforms.validators import DataRequired,Email,EqualTo , Length
from wtforms import ValidationError
from flask_login import current_user
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email(),Length(min=10, max=40)])
    username = StringField('Username', validators=[DataRequired(),Length(min=6, max=30)] )
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!'),Length(min=6, max=30)])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired(),Length(min=6, max=30)])
    name = StringField('Name', validators=[DataRequired(), Length(min=6, max=30)] )
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=11, max=11)])
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
    email = StringField('Email')
    name = StringField('Name')
    phone = StringField('Phone Number')
    date = DateField('Pick a date',validators=[DataRequired()] , format= '%Y-%m-%d' )
    time = SelectField(u'Time', choices=[('08', '8 AM'), ('09', '9 AM'), ('10', '10 AM'),('11', '11 AM'),('12', '12 PM'),('13', '1 PM') , ('14', '2 PM'),('15', '3 PM'),('16', '4 PM')] , validators=[DataRequired()])
    submit = SubmitField('Submit')



class UpdateUserForm(FlaskForm):
    image = FileField('Update Profile Picture')
    submit = SubmitField('Update')

        # Check if not None for that user email!
    def validate_email(self, email):
        if(current_user.email == email.data):
            pass

        elif User.query.filter_by(email=email.data).first():
            raise ValidationError('Email has been registered')



class UpdateScan(FlaskForm):
    image = FileField('Update Profile Picture', validators=[DataRequired()])
    submit = SubmitField('Add Scan')

class BlogPostForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')
