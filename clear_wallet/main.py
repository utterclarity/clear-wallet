# -*- coding: utf-8 -*-
import gevent.monkey
gevent.monkey.patch_all()

import json

from flask import Flask, render_template, session
from flask import url_for, redirect, flash, jsonify, abort
from flask import Response, stream_with_context
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, IntegerField
import blcpy


app = Flask(__name__)
with open('config.json', 'rb') as f:
    config = json.load(f)
    app.config.update(**config)
    app.config['SECRET_KEY'] = str(config['SECRET_KEY'])


class LoginForm(Form):
    address = TextField("Address")
    passkey = PasswordField("Passkey")


class SendForm(Form):
    address = TextField("Address of receiver")
    amount = IntegerField("Amount")


def gather_data():
    data = {
        "coins": None,
        "transactions": None,
    }
    q = blcpy.CheckAddr(addr=session['address'])
    try:
        data['coins'] = q()
    except blcpy.BLCException:
        pass
    q = blcpy.Transactions(addr=session['address'], pwd=session['passkey'])
    try:
        data['transactions'] = q()
    except blcpy.BLCException:
        pass
    return data


def register_new_address(repeats=3):
    import uuid
    import hashlib
    addr, pwd = "", ""
    for _ in xrange(repeats):
        addr = hashlib.sha1(str(uuid.uuid4())).hexdigest()
        pwd = hashlib.sha1(str(uuid.uuid4())).hexdigest()
        q = blcpy.Register(addr=addr, pwd=pwd)
        try:
            # Unused return, throws exception on failure.
            q()
            return (addr, pwd)
        except blcpy.BLCException:
            continue
    return (False, False)


@app.route("/bloostamp/get")
def bloostamp_get():
    if "logged_in" not in session or session['logged_in'] is not True:
        abort(403)

    def generator():
        yield "{0}:{1}:{2}".format(
            session['address'],
            session['passkey'],
            "CW"
        )
    return Response(
        stream_with_context(generator()),
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment;filename=bloostamp"
        })


@app.route("/bloostamp/up", methods=["POST"])
def bloostamp_up():
    abort(403)


@app.route("/bloostamp/generate", methods=["POST"])
def bloostamp_generate():
    if "logged_in" in session:
        return jsonify({"success": False, "url": "1"})
    addr, pwd = register_new_address()
    if addr is False and pwd is False:
        return jsonify({"success": False, "url": "2"})
    session['logged_in'] = True
    session['address'] = addr
    session['passkey'] = pwd
    flash("Successfully generated a new BlooCoin address!", "success")
    return jsonify({
        "success": True,
        "url": url_for('index')
    })


@app.route("/data.json")
def data_json():
    if "logged_in" not in session or session['logged_in'] is not True:
        return jsonify({})
    return jsonify(gather_data())


@app.route("/", methods=["GET", "POST"])
def index():
    if "logged_in" not in session or session['logged_in'] is not True:
        return redirect(url_for("login"))
    send_blc = SendForm()
    if send_blc.validate_on_submit():
        q = blcpy.SendCoin(**{
            "to": send_blc.address.data,
            "addr": session['address'],
            "pwd": session['passkey'],
            "amount": send_blc.amount.data
        })
        try:
            d = q()
            msg = "Successfully sent {0} {1} BLC!"
            flash(msg.format(d['to'], d['amount']), "success")
        except blcpy.CommandFailure:
            msg = "Failed! Server says: {0}".format(q.data['message'])
            flash(msg, "error")
        except blcpy.BLCException:
            flash("Something went wrong talking to the server!", "error")
    return render_template(
        "index.html",
        addr=session['address'],
        send_blc=send_blc
    )


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
        q = blcpy.MyCoins(addr=address, pwd=passkey)
        try:
            q()
            session['logged_in'] = True
            session['address'] = address
            session['passkey'] = passkey
            flash("Successfully logged in as: {0}".format(address), "success")
            return redirect(url_for("index"))
        except blcpy.SocketException:
            flash("Unable to contact server!", "error")
        except blcpy.BLCException:
            flash("Error communicating with server!", "error")
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run()
