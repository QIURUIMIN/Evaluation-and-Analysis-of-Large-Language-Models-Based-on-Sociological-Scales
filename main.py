#!user/bin/env python3
# -*- coding: gbk -*-
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    with open("static/Homepage.html", encoding='utf-8') as f:
        content = f.read()
    return content

@app.route("/Scales")
def Scales():
    with open("static/Scales.html", encoding='utf-8') as f:
        content = f.read()
    return content

@app.route("/LLM")
def LLM():
    with open("static/LLM.html", encoding='utf-8') as f:
        content = f.read()
    return content

@app.route("/Interactive")
def Interactive():
    with open("static/Interactive.html", encoding='utf-8') as f:
        content = f.read()
    return content



#运行应用程序

if __name__ == "__main__":
    app.run()

#查看当前flask的所有路由以及函数对应的关系（这其实就是路由）
#print(app.url_map)


