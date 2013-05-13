# -*- coding: utf-8 -*-
import sys
import json
import socket

from flask import Flask, render_template, request, g, session
from flask import url_for, redirect, flash
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField

app = Flask(__name__)
app.debug = "--debug" in sys.argv
with open('config.json', 'rb') as f:
    config = json.load(f)
    app.config.update(**config)
    # Specifically this causes shitloads of issues if it's not str()
    app.config['SECRET_KEY'] = str(config['SECRET_KEY'])


class LoginForm(Form):
    address = TextField("Address")
    passkey = PasswordField("Passkey")


class VerifyAccount(object):
    def __init__(self,
                 address,
                 passkey,
                 timeout=1,
                 retries=0,
                 server=("server.bloocoin.org", 3122)):
        self.address = address
        self.passkey = passkey
        self._timeout = timeout
        # Not actually used. -- TODO
        self._retries = retries
        self._server = server
        self._buffer = 1024  # non-negotiable, bugger off.
        # Error codes, yo.
        self._code = 0

    def _validate(self):
        """ Should test that address/pass are valid.
            Length is the main thing to check.
        """
        # some_tests(self.address, self.passkey)
        pass

    def verify(self):
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect(self._server)
            s.send(json.dumps({
                "cmd": "my_coins",
                "addr": self.address,
                "pwd": self.passkey
            }))
            rec = s.recv(self._buffer)
            rec = json.loads(rec)
            if rec['success']:
                self._validate()
                return True
        except socket.error as e:
            self._code = 1
            return False
        except ValueError as e:
            # JSON decoding error, probably.
            self._code = 2
            return False
        self._code = 3
        return False


@app.route("/")
def index():
    if "logged_in" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", addr=session['address'])


@app.route("/logout")
def logout():
    session.clear()
    flash("You were logged out.", "info")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        address = form.address.data
        passkey = form.passkey.data
        v = VerifyAccount(address, passkey)
        if v.verify():
            session['logged_in'] = True
            session['address'] = address
            session['passkey'] = passkey
            # To stop hijacking - not without Flask-KVSessions tho
            #session.regenerate()
            flash("Successfully logged in for: {0}".format(address), "success")
            return redirect(url_for("index"))
        else:
            if v._code == 1:
                flash("Unable to contact server!", "error")
            elif v._code == 2:
                flash("Error communicating with server!", "error")
            elif v._code == 3:
                flash("Misc. problem talking to server!", "error")
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run()
