from flask import render_template, url_for, flash, redirect, Response, request, send_from_directory
from services import app, bcrypt, login_manager
from services.forms import RegistrationForm, LoginForm, ContactForm, BookAppointmentForm, scanForm
from flask_login import UserMixin
import sqlite3
from flask_login import login_user, current_user, logout_user, login_required
from services.models import User, Account, Image

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/img/<email>')
def serve_img(email):
    img = Account.get_img(email)
    if not img:
        return "url_for('static', filename='images/default-img.png')"
    print('************************************************')
    return Response(img.img, img.mimetype)
    #< img src = "{{ url_for('serve_img', email=current_user.email )}}" >
# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route('/')
def root():
    return redirect(url_for('home'))

# **************************************************************************
#                             HOME
# **************************************************************************
@app.route('/home')
def home():
    return render_template("home.html")


# **************************************************************************
#                             ABOUT
# **************************************************************************
@app.route('/about/<int:templateId>')
def about(templateId):
    if templateId == 0:
        return render_template("aboutus.html")
    if templateId == 1:
        return render_template("aboutus2.html")
    if templateId == 2:
        return render_template("aboutus3.html")


# **************************************************************************
#                             REGISTER
# **************************************************************************
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        Account.create(  username = form.username.data,
                         email = form.email.data,
                         name = form.name.data,
                         phone = form.phone.data,
                         password = form.password.data,
                         type = form.type.data)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    flash('there is an error, please try again later', 'danger')
    return render_template('register.html',title='register' , form=form)

# **************************************************************************
#                             LOGIN
# **************************************************************************
@app.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated():
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@his.com' and form.password.data == 'admin':
            user = User.getUser(form.email.data)
            if not user:
                user = User('admin', 'admin@his.com', './admin.png', 'admin')
            login_user(user, remember=form.remember.data)
            flash('You have been logged in! Welcome Admin', 'success')
            return redirect(url_for('home'))
        else:
            user = User.getUser(form.email.data)
            if user:
                hashed_password = User.getPassword(user)
                if bcrypt.check_password_hash(hashed_password, form.password.data):
                    #the user exist and the password is matched
                    login_user(user, remember=form.remember.data)
                    flash(f'You have been logged in! Welcome {user.username}', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Login Unsuccessful. Please check username and password', 'danger')
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

# **************************************************************************
#                             LOGOUT
# **************************************************************************
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/account", methods=['POST', 'GET'])
def account(usr):
    if request.method == 'POST':
        pic = request.files['pic']
        Account.set_img(current_user.email, pic)
    return render_template('account.html', title='Account')

# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/users", methods=['POST', 'GET'])
@login_required
def users(usr):
    ## init the database
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users''')
    row_headers = [x[0] for x in cur.description]
    table = cur.fetchall()
    return render_template('users.html', title='users', headers= row_headers, data= table)

# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/forms", methods=['POST', 'GET'])
@login_required
def forms(usr):
    ## init the database
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM form''')
    # row_headers = [x[0] for x in cur.description]
    table = cur.fetchall()
    return render_template('forms.html', title='forms', data= table)

# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/appointments")
@login_required
def appointments(usr):
    return redirect(url_for('home'))
# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/patients")
@login_required
def patients(usr):
    return redirect(url_for('home'))
# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/doctors")
@login_required
def doctors(usr):
    return redirect(url_for('home'))
# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/scans")
@login_required
def scans(usr):
    return redirect(url_for('home'))
# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/calender")
@login_required
def calendar(usr):
    return redirect(url_for('home'))
