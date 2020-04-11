from flask import Flask, render_template, session, g, flash
import time

app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def index():
    session['user'] = "游客"
    g.db = "mysql"
    return render_template('02上下文环境.html')


@app.context_processor
def appinfo():
    data = {
        'cate1': '爬虫',
        'cate2': '数据分析',
        'cate3': '人工智能'
    }
    return dict(data=data)


@app.context_processor
def get_current_time():
    def get_time(timeFormat="%Y-%m-%d - %H:%M:%S"):
        return time.strftime(timeFormat)

    return dict(current_time=get_time)
