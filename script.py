from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/about')
def about_function():
    return '<h1>About!</h1>'

if __name__ == "__main__":
    app.run(debug=True)
