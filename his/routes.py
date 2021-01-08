from flask import render_template, url_for, flash, redirect
from his import app
from his.forms import RegistrationForm, LoginForm
from his.authors import authors
from his import conn

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route('/')
def hello_world():
    return render_template("home.html")

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route('/about')
def about_function():
    return render_template("about.html", authors=authors, title="About")

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
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
