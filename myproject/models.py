from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    job = db.Column(db.String)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(11), unique=True, index=True)
    doctor_rel = db.relationship('D_accounts',backref='user',uselist=False)
    patient_rel = db.relationship('P_accounts',backref='user',uselist=False)



    def __init__(self, email, username, password , job , name):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.job = job
        self.name = name
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class D_accounts(db.Model):
    __tablename__ = "d_accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, db.ForeignKey('users.email'))
    name = db.Column(db.String(64))
    phone = db.Column(db.String(11), unique=True, index=True)
    def __init__(self , email , name , phone):
        self.email = email
        self.name = name
        self.phone = phone

class P_accounts(db.Model):
    __tablename__ = "p_accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, db.ForeignKey('users.email'))
    name = db.Column(db.String(64))
    phone = db.Column(db.String(11), unique=True, index=True)
    scan_rel = db.relationship('Scans',backref='p_accounts' , lazy='dynamic')
    def __init__(self , email , name , phone):
        self.email = email
        self.name = name
        self.phone = phone

class Contact(db.Model):
    __tablename__ ="forms"
    id = db.Column(db.Integer, primary_key=True)
    script = db.Column(db.Text)
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
    file_url = db.Column(db.String)
