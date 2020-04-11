from flask import Flask, render_template

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')

@app.route('/')
@app.route('/hello/<name>')
def index(name=None):
    if not name:
        name = '<em>World</em>'
    return render_template('01流程控制.html',
                           name=name,
                           digits=[1, 2, 3, 4, 5],
                           users=[{'name': 'John'},
                                  {'name': 'Tom', 'hidden': True},
                                  {'name': 'Lisa'},
                                  {'name': 'Bob'}])
