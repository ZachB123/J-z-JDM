import os
from config import Config
from flask import Flask, render_template
from dotenv import load_dotenv
load_dotenv()
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)

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

@app.route("/Accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/Privacy-Policy")
def privacyPolicy():
    return render_template("privacyPolicy.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

