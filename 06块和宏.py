from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    hello = "hello world !"
    return render_template('06块和宏.html', hello=hello)
