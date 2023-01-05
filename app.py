import os
from config import Config
from flask import Flask, render_template, redirect, url_for, flash
from dotenv import load_dotenv
load_dotenv()
from forms import LoginForm
from flask_login import LoginManager, current_user, login_user, logout_user
from models import User

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "Login"
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
        return redirect(url_for("index"))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register")
def register():
    pass

@app.route("/profile")
def profile():
    return render_template("profile.html")


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

@app.route("/Accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/Privacy-Policy")
def privacyPolicy():
    return render_template("privacyPolicy.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

