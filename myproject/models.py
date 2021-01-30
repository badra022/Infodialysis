from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64))
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String)
    job = db.Column(db.String)
    name = db.Column(db.String(64))
    phone = db.Column(db.String)
    profile_image = db.Column(db.String)
    doctor_rel = db.relationship('D_accounts',backref='duser',uselist=False)
    patient_rel = db.relationship('P_accounts',backref='puser',uselist=False)
    blog_rel = db.relationship('BlogPost',backref='post' , lazy='dynamic')

    def __init__(self, email, username, password , job , name , phone , profile_image):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.job = job
        self.name = name
        self.phone = phone
        self.profile_image= profile_image
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Welcome {self.username}"




class D_accounts(db.Model):
    __tablename__ = "d_accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, db.ForeignKey('users.email'))
    username = db.Column(db.String(64))
    name = db.Column(db.String(64))
    phone = db.Column(db.String)
    def __init__(self , email ,username , name , phone):
        self.email = email
        self.username = username
        self.name = name
        self.phone = phone

class P_accounts(db.Model):
    __tablename__ = "p_accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, db.ForeignKey('users.email'))
    username = db.Column(db.String(64))
    name = db.Column(db.String(64))
    phone = db.Column(db.String)
    scan_rel = db.relationship('Scans',backref='p_scan' , lazy='dynamic')
    def __init__(self , email, username , name , phone):
        self.email = email
        self.username = username
        self.name = name
        self.phone = phone


class BlogPost(db.Model):
    __tablename__ = "blogposts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, text, user_id):
        self.text = text
        self.user_id =user_id


class Contact(db.Model):
    __tablename__ ="forms"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(64))
    name = db.Column(db.String(64))
    def __init__(self , text , email , name):
        self.text = text
        self.email = email
        self.name = name

class Scans(db.Model):
    __tablename__ ="scans"
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer , db.ForeignKey('p_accounts.id'))
    scan = db.Column(db.String)
    def __init__(self , p_id , scan):
        self.p_id = p_id
        self.scan = scan





class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    date = db.Column(db.String)
    def __init__(self , email ,name ,phone ,date):
        self.email = email
        self.name =  name
        self.phone = phone
        self.date = date
######
