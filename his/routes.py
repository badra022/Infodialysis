from flask import render_template, url_for, flash, redirect
from his import app, bcrypt, login_manager
from his.forms import RegistrationForm, LoginForm
from his.authors import authors
from flask_login import UserMixin
import sqlite3
from flask_login import login_user, current_user, logout_user, login_required



newDoctorAccountScript = '''INSERT INTO doctor_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''
newPatientAccountScript = '''INSERT INTO doctor_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''
newUserScript = '''INSERT INTO users (username, email) VALUES (?,?)'''

# # init the database
# conn = sqlite3.connect('database.sqlite')
# cur = conn.cursor()


class User:
    def __init__(self, username, email, img_file):
        self.username = username
        self.email = email
        self.img_file = img_file
        ## init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''
        SELECT id FROM users WHERE username = ? AND email = ?
        ''', (self.username, self.email, ))
        # conn.commit()
        try:
            self.id = cur.fetchone()[0]
        except:
            self.id = -1

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    @classmethod
    def get_by_id(self, user_id):
        ## init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        q_res = cur.execute('''
        SELECT username, email, img_file FROM users WHERE id = ?
        ''', (user_id,)).fetchone()
        u = User(q_res[0], q_res[1], q_res[2])
        return u

# # for usage of flask_login
# class User(UserMixin):
#     # def __init__(username, email, img_file):
#     #     self.username= username
#     #     self.email= email
#     #     self.image_file= img_file
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"

@login_manager.user_loader
def load_user(user_id):
    # # # init the database
    # conn = sqlite3.connect('database.sqlite')
    # cur = conn.cursor()
    # cur.execute('''SELECT username, email, img_file FROM users WHERE id=?''', (int(user_id),))
    # try:
    #     return User(username=cur.fetchone()[0], email=cur.fetchone()[1], image_file=cur.fetchone()[2])
    # except:
    #     pass
    # pass
    return User.get_by_id(user_id)

def getUser(email):
    # # init the database
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    print("retrieving the user account from doctors and patients accounts....")
    cur.execute('''SELECT username, email FROM doctor_account WHERE email=?''', (email,))
    try:
        print("found in doctors accounts!")
        result = cur.fetchone()
        return User(result[0], result[1], 'None')
    except:
        pass
    cur.execute('''SELECT username, email FROM patient_account WHERE email=?''', (email,))
    try:
        result = cur.fetchone()
        return User(result[0], result[1], 'None')
    except:
        pass
    return None

def getPassword(user):
    # # init the database
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT password FROM doctor_account WHERE email=?''', (user.email,))
    try:
        return cur.fetchone()[0]
    except:
        pass
    cur.execute('''SELECT password FROM patient_account WHERE email=?''', (user.email,))
    try:
        return cur.fetchone()[0]
    except:
        pass
    pass

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.doctor.data:
            # cur = conn.cursor()
            cur.execute(newDoctorAccountScript, (form.username.data,
                                                 form.email.data,
                                                 form.name.data,
                                                 form.phone.data,
                                                 hashed_password, ))
            conn.commit()
            cur.execute(newUserScript, (form.username.data, form.email.data, ))
            conn.commit()
        elif form.patient.data:
            # cur = conn.cursor()
            cur.execute(newPatientAccountScript, (form.username.data,
                                                 form.email.data,
                                                 form.name.data,
                                                 form.phone.data,
                                                 hashed_password, ))
            conn.commit()
            cur.execute(newUserScript, (form.username.data, form.email.data, ))
            conn.commit()
        else:
            flash('please select type of account, patient or doctor!', 'danger')
            return render_template('register.html', title='Register', form=form)

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# **************************************************************************
#                             ROOT
# **************************************************************************
@app.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated():
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@his.com' and form.password.data == 'admin':
            print("---------------------------------")
            user = getUser(form.email.data)
            if not user:
                ## init the database
                conn = sqlite3.connect('database.sqlite')
                cur = conn.cursor()
                cur.execute(newUserScript, ('admin', 'admin@his.com', ))
                conn.commit()
                user = User('admin', 'admin@his.com', './admin.png')
            login_user(user, remember=form.remember.data)
            flash('You have been logged in! Welcome Admin', 'success')
            return redirect(url_for('home'))
        else:
            user = getUser(form.email.data)
            if user:
                hashed_password = getPassword(user)
                if bcrypt.check_password_hash(hashed_password, form.password.data):
                    #the user exist and the password is matched
                    login_user(user, remember=form.remember.data)
                    flash(f'You have been logged in! Welcome {user.username}', 'success')
                    # next_page = request.args.get('next')
                    return redirect(url_for('home'))
                else:
                    flash('Login Unsuccessful. Please check username and password', 'danger')
            # flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')















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
