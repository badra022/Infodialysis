from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] =  '5791628bb0b13ce0c676dfde280ba245'

authors = [
    {
    'name':'Ahmed Badra',
    'summary':''' 3rd year college student working towards a Bachelor in systems and biomedical engineering''',
    'core_skills':['C', 'embedded systems', 'Autosar', 'OOP', 'c++', 'python', 'data structure', 'SQL']
    },
    {
    'name':'Hassan Fathi',
    'summary':''' 3rd year college student working towards a Bachelor in systems and biomedical engineering''',
    'core_skills':['C', 'embedded systems', 'Autosar', 'OOP', 'c++', 'python', 'data structure', 'SQL']
    },
    {
    'name':'Ammar Elsaeed',
    'summary':''' 3rd year college student working towards a Bachelor in systems and biomedical engineering''',
    'core_skills':['C', 'embedded systems', 'Autosar', 'OOP', 'c++', 'python', 'data structure', 'SQL']
    },
    {
    'name':'Ahmed Sayed',
    'summary':''' 3rd year college student working towards a Bachelor in systems and biomedical engineering''',
    'core_skills':['C', 'embedded systems', 'Autosar', 'OOP', 'c++', 'python', 'data structure', 'SQL']
    },
    {
    'name':'Youssef Mohamed',
    'summary':''' 3rd year college student working towards a Bachelor in systems and biomedical engineering''',
    'core_skills':['C', 'embedded systems', 'Autosar', 'OOP', 'c++', 'python', 'data structure', 'SQL']
    }
]

@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/about')
def about_function():
    return render_template("about.html", authors=authors, title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


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


if __name__ == "__main__":
    app.run(debug=True)
