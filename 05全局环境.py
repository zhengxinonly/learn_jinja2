import time

from flask import Flask, render_template
import re

app = Flask(__name__)


@app.route('/')
def index():
    hello = "hello world !"
    return render_template('05全局函数.html', hello=hello)


def accept_pattern(pattern_str):
    pattern = re.compile(pattern_str, re.S)

    def search(content):
        return pattern.findall(content)

    return dict(search=search, current_pattern=pattern_str)


app.add_template_global(accept_pattern, 'accept_pattern')


@app.template_global('current_time')
def current_time(timeFormat="%Y-%m-%d - %H:%M:%S"):
    return time.strftime(timeFormat)
