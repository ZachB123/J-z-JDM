import os
from config import Config
from flask import Flask, render_template, redirect, url_for, flash, request
from dotenv import load_dotenv
load_dotenv()
from forms import LoginForm, RegistrationForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import User
from werkzeug.urls import url_parse
from database import db

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "login"
# login.init_app(app)

@login.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    # TODO make it so you return to the page you were on
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        db.create_user(User(form.username.data, form.email.data, form.password.data))
        flash("Cogratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/profile")
@login_required
def profile():
    user = User.get_by_id(int(current_user.get_id()))
    return render_template("profile.html", user=user)

@app.route("/company")
def company():
    return render_template("company.html")

@app.route("/listings")
def listings():
    return render_template("listings.html")

@app.route("/car")
def car():
    return render_template("car.html")

@app.route("/loan")
def loan():
    return render_template("loan.html")

@app.route("/control")
@login_required
def control():
    if User.get_by_id(int(current_user.get_id())).super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    return render_template("control.html")

@app.route("/Accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/Privacy-Policy")
def privacyPolicy():
    return render_template("privacyPolicy.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

