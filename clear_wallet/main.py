# -*- coding: utf-8 -*-
import sys
import json

from flask import Flask, render_template, request, g
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField

app = Flask(__name__)
app.debug = "--debug" in sys.argv
with open('config.json', 'rb') as f:
    config = json.load(f)
    #app.config.update(**config)
    app.config['SECRET_KEY'] = str(config['SECRET_KEY'])

class LoginForm(Form):
    address = TextField("Address")
    passkey = PasswordField("Passkey")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run()
