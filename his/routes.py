from flask import render_template, url_for, flash, redirect
from his import app
from his.forms import RegistrationForm, LoginForm
from his.authors import authors
import sqlite3


newDoctorAccountScript = '''INSERT INTO doctor_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''
newPatientAccountScript = '''INSERT INTO doctor_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''

# init the database
conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route('/')
def home():
    return render_template("home.html")

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route('/about')
def about():
    return render_template("about.html", authors=authors, title="About")

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        if form.doctor.data:
            # cur = conn.cursor()
            cur.execute(newDoctorAccountScript, (form.username.data,
                                                 form.email.data,
                                                 form.name.data,
                                                 form.phone.data,
                                                 form.password.data, ))
            conn.commit()
        elif form.patient.data:
            # cur = conn.cursor()
            cur.execute(newPatientAccountScript, (form.username.data,
                                                 form.email.data,
                                                 form.name.data,
                                                 form.phone.data,
                                                 form.password.data, ))
            conn.commit()
        else:
            flash('please select type of account, patient or doctor!', 'danger')
            return render_template('register.html', title='Register', form=form)

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@his.com' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

















# def class User:
#     def __init__(self, name, phone, username, password, email, FformID, DdoctorID, FpatientID):
#         script = '''INSERT INTO Accounts (name, phone, username, password, email, FformID, DdoctorID, FpatientID)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
#         val = (name, phone, username, password, email, FformID, DdoctorID, FpatientID)
#         self.name = name
#         self.phone = phone
#         self.username = username
#         self.password = password
#         self.email = email
#         self.FformID = FformID
#         self.DdoctorID = DdoctorID
#         self.FpatientID = FpatientID
#         cur.execute(script, val)
#         mydb.commit()
#
