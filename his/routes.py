from flask import render_template, url_for, flash, redirect
from his import app, bcrypt, login_manager
from his.forms import RegistrationForm, LoginForm
from his.authors import authors
from flask_login import UserMixin
import sqlite3
from flask_login import login_user, current_user, logout_user, login_required
from his.models import User


# sqlite scripts that handles the insertion to the system database
newDoctorAccountScript = '''INSERT INTO doctor_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''
newPatientAccountScript = '''INSERT INTO patient_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''
newUserScript = '''INSERT INTO users (username, email,type) VALUES (?,?,?)'''


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

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
@app.route('/about')
def about():
    return render_template("about.html", authors=authors, title="About")

# **************************************************************************
#                             REGISTER
# **************************************************************************
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.doctor.data:
            # cur = conn.cursor()
            cur.execute(newDoctorAccountScript, (form.username.data,
                                                 form.email.data,
                                                 form.name.data,
                                                 form.phone.data,
                                                 hashed_password, ))
            conn.commit()
            cur.execute(newUserScript, (form.username.data, form.email.data, 'doctor', ))
            conn.commit()
        elif form.patient.data:
            # cur = conn.cursor()
            cur.execute(newPatientAccountScript, (form.username.data,
                                                 form.email.data,
                                                 form.name.data,
                                                 form.phone.data,
                                                 hashed_password, ))
            conn.commit()
            cur.execute(newUserScript, (form.username.data, form.email.data, 'patient', ))
            conn.commit()
        else:
            flash('please select type of account, patient or doctor!', 'danger')
            return render_template('register.html', title='Register', form=form)

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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
                ## init the database
                conn = sqlite3.connect('database.sqlite')
                cur = conn.cursor()
                cur.execute(newUserScript, ('admin', 'admin@his.com', 'admin'))
                conn.commit()
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
                    # next_page = request.args.get('next')
                    return redirect(url_for('home'))
                else:
                    flash('Login Unsuccessful. Please check username and password', 'danger')
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

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
@app.route("/<usr>/account")
@login_required
def account(usr):
    return render_template('account.html', title='Account')

# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/users")
@login_required
def users(usr):
    return redirect(url_for('home'))
# **************************************************************************
#                             ACCOUNT
# **************************************************************************
@app.route("/<usr>/forms")
@login_required
def forms(usr):
    return redirect(url_for('home'))
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
def calender(usr):
    return redirect(url_for('home'))
