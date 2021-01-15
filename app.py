from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort , send_from_directory
from flask_login import login_user,login_required,logout_user , current_user
from myproject.models import User , Contact , D_accounts , P_accounts , Scans , Appointment , BlogPost
from myproject.forms import LoginForm, RegistrationForm , ContactForm ,UpdateUserForm , UpdateScan , BookAppointment, BlogPostForm
from myproject.drc import create_event
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from PIL import Image
from datetime import datetime





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


        if (form.email.data == "admin@admin.com" and form.password.data == "admin" and user is None):
            user = User(email=form.email.data,
                        username="admin",
                        password=form.password.data,
                        job = "admin",
                        name = "admin",
                        phone = "123",
                        profile_image = "default_profile.jpg"
                        )

            db.session.add(user)
            db.session.commit()


        if user is not None :

            if user.check_password(form.password.data) :
            #Log in the user

                login_user(user)
                flash('Logged in successfully.')

                next = request.args.get('next')

                if next == None or not next[0]=='/':
                    next = url_for('home')

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
                    phone = form.phone.data,
                    profile_image = "default_profile.jpg"

                    )

        db.session.add(user)
        db.session.commit()
        if (form.job.data == 'patient'):
            patient = P_accounts(email=form.email.data,
                                 username=form.username.data,
                                 name = form.name.data,
                                 phone = form.phone.data
                                 )
            db.session.add(patient)
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

#####################################################################################
####################################update account##################################

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["IMAGE_UPLOADS"] = os.path.join(basedir, 'myproject/static')

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]

def allowed_image(filename):

    ext = filename.split('.')[-1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = current_user.email).first()
        if form.image.data:


            image = form.image.data
            if allowed_image(image.filename):
                filename = current_user.username + "." + image.filename.split('.')[-1]
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],'profile_pics' ,filename))

                user.profile_image = filename

            else:
                flash("That file extension is not allowed")
                return redirect(url_for('account'))

        db.session.add(user)
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('account'))



    return render_template("account.html" , form=form)
###################################################################################
###############################book an appointment for patient#####################
###################################################################################
@app.route('/bookappointment', methods=["GET", "POST"])
def bookappointment():
    form = BookAppointment()
    doctors = D_accounts.query.all()
    attendees=[]
    for doctor in doctors:
        attendee = {'email': doctor.email }
        attendees.append(attendee)
    if form.validate_on_submit():
        time = str(form.date.data) + " " + str(form.time.data)
        if  Appointment.query.filter_by(date=time).first() or time < str(datetime.utcnow()) :
            flash('This appointment is not available')
            return redirect(url_for('bookappointment'))
        else:
            if current_user.is_authenticated:
                ap = Appointment(email = current_user.email,
                                 name = current_user.name,
                                 phone = current_user.phone,
                                 date = time
                                )
                db.session.add(ap)
                db.session.commit()

            else:

                ap = Appointment(email = form.email.data,
                                 name = form.name.data,
                                 phone = form.phone.data,
                                 date = time
                                )
                db.session.add(ap)
                db.session.commit()

            create_event(time , attendees )
            flash('The appointment has been booked successfully!')
            return redirect(url_for('home'))

    return render_template('bookappointment.html' , form = form)


###################################################################################
################################patient appointment###############################
#################################################################################
@app.route("/patientsappointments/<email>", methods=["GET", "POST"])
@login_required
def patientsappointments(email):
    aps = Appointment.query.filter_by(email=email).order_by(Appointment.id.desc())
    return render_template('patientsappointments.html', aps=aps )
#################################################################################
##################################appointments###################################
#################################################################################
@app.route("/patientsappointments", methods=["GET", "POST"])
@login_required
def appointments():
    aps = Appointment.query.order_by(Appointment.id.desc())
    return render_template('appointments.html', aps=aps )


##################################################################################
#################################admin stuff #####################################
##################################################################################
####################################patient list##################################
@app.route("/patientslist", methods=["GET", "POST"])
@login_required
def patientslist():
    patients = P_accounts.query.all()
    return render_template('patientsList.html', patients=patients)


###################################patient info and upload scan####################

@app.route("/patientinfo/<username>", methods=["GET", "POST"])
@login_required
def patientinfo(username):
    user = User.query.filter_by(username=username).first_or_404()
    patient = P_accounts.query.filter_by(puser=user).first()
    form = UpdateScan()

    if form.validate_on_submit():
        if form.image.data:
            image = form.image.data
            if allowed_image(image.filename):
                filename = image.filename
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],'scans' , filename))

                scan = Scans(p_id = patient.id,
                             scan = filename
                            )
                db.session.add(scan)
                db.session.commit()
                flash("Scan saved")

            else:
                flash("That file extension is not allowed")
        else:
            flash("No Scan has been chosen")


    return render_template('patientInfo.html', patient=patient , user=user , form=form)

###################################doctors list######################################
@app.route("/doctorslist", methods=["GET", "POST"])
@login_required
def doctorslist():
    doctors = D_accounts.query.all()
    return render_template('doctorslist.html', doctors=doctors)
###############################doctor info#########################################
@app.route("/doctorinfo/<username>", methods=["GET", "POST"])
@login_required
def doctorinfo(username):
    user = User.query.filter_by(username=username).first_or_404()
    doctor = D_accounts.query.filter_by(duser=user).first()
    return render_template('doctorinfo.html', doctor=doctor , user=user)
#############################messages###############################################
@app.route("/msgs", methods=["GET", "POST"])
@login_required
def msgs():
    msgs = Contact.query.order_by(Contact.date.desc())
    return render_template('msgs.html', msgs=msgs)

########################################Download####################################
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.config["IMAGE_UPLOADS"],'scans')
    return send_from_directory(directory=uploads, filename=filename)
####################################################################################
####################################view scans for patient#########################
####################################################################################
@app.route("/patientscans/<username>", methods=["GET", "POST"])
@login_required
def patientscans(username):
    patient = P_accounts.query.filter_by(username=username).first_or_404()
    scans = Scans.query.filter_by(p_id = patient.id).order_by(Scans.id.desc())
    return render_template('patientScans.html', scans=scans , patient = patient)
####################################################################################
##################################doctors blog######################################
####################################################################################
@app.route('/blog', methods=["GET", "POST"])
def blog():
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc())
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('blog'))
    return render_template('blog.html',blog_posts=blog_posts , form = form)




@app.route("/<int:blog_post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('blog'))

###########################################################################################################################################################################
if __name__ == '__main__':
    app.run(debug=True)
