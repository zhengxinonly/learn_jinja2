from flask import Flask, render_template
import re

app = Flask(__name__)


@app.route('/')
def index():
    hello = "hello world !"
    return render_template('04测试器.html', hello=hello)


def has_number(str):
    return re.match('.*\d+', str)


app.add_template_test(has_number, 'contain_number')


@app.template_test('end_with')
def end_with(str, suffix):
    return str.lower().endswith(suffix.lower())
