from flask import render_template, flash, redirect, url_for
from app import app

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/listings")
def listings():
    return render_template("listings.html")

@app.route("/car")
def car():
    return render_template("car.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/management")
def management():
    return render_template("management.html")

@app.route("/loan")
def loan():
    return render_template("loan.html")

@app.route("/control")
def control():
    return render_template("control.html")