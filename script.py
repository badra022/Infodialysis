from flask import Flask, render_template
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
