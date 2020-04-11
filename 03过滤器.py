from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    hello = "hello world !"
    return render_template('03过滤器.html', hello=hello)


@app.template_filter('double_step')
def double_filter(l):
    r = filter(lambda x: x % 2 == 0, l)
    return list(r)


# app.add_template_filter(double_filter, 'double_step')
