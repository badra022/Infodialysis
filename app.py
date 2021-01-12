from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User , Contact , D_accounts , P_accounts
from myproject.forms import LoginForm, RegistrationForm , ContactForm
from werkzeug.security import generate_password_hash, check_password_hash



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/aboutus2')
def aboutus2():
    return render_template('aboutus2.html')

@app.route('/aboutus3')
def aboutus3():
    return render_template('aboutus3.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
        if (form.email.data == "admin@admin.com" and form.password.data == "admin" and user is None):
            user = User(email=form.email.data,
                        username="admin",
                        password=form.password.data,
                        job = "admin",
                        name = "admin",
                        phone = "123"
                        )

            db.session.add(user)
            db.session.commit()


        if user is not None :

            if user.check_password(form.password.data) :
            #Log in the user

                login_user(user)
                flash('Logged in successfully.')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0]=='/':
                    next = url_for('welcome_user')

                return redirect(next)

            else:
                flash('Password is not correct')

        else:
                flash('Email is not correct')


    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    job = form.job.data,
                    name = form.name.data,
                    phone = form.phone.data

                    )

        db.session.add(user)
        db.session.commit()
        if (form.job.data == 'patient'):
            patient = P_accounts(email=form.email.data,
                                 username=form.username.data,
                                 name = form.name.data,
                                 phone = form.phone.data
                                 )
            db.session.add(patint)
            db.session.commit()
        else:
            doctor = D_accounts(email=form.email.data,
                                 username=form.username.data,
                                 name = form.name.data,
                                 phone = form.phone.data
                                 )
            db.session.add(doctor)
            db.session.commit()

        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))


    return render_template('register.html', form=form)

#################################
###########error pages##########
################################
@app.errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html') , 404




@app.errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html') , 403

@app.route('/contact', methods=['GET', 'POST'])



def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(text = form.text.data,
                          email = form.email.data,
                          name = form.name.data
                          )
        db.session.add(contact)
        db.session.commit()
        flash('Thanks for your meassage')
        return redirect(url_for('home'))
    return render_template('contact.html', form=form)





if __name__ == '__main__':
    app.run(debug=True)
