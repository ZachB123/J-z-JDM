import os
from models import User, Car, Image, SalesRep, ContactMessage, DirectMessage, DirectDatabaseDirectMessage, refresh_database, close_database
from config import Config
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from dotenv import load_dotenv
load_dotenv()
from forms import LoginForm, UpdateEmail, RegistrationForm, CarCreationForm, AddImages, ConfigureSalesRep, Contact, DirectMessageForm, Search, ResetPassword, ResetPasswordEmail
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import json
from flask_sslify import SSLify
from jwttoken import get_reset_password_token, verify_reset_password_token
from flask_mail import Message
from flask_mail_sendgrid import MailSendGrid
import threading

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "login"

# https://pypi.org/project/Flask-Mail-SendGrid/
mail = MailSendGrid(app)

# uncomment for production
# sslify = SSLify(app)

def send_email(subject="subject", sender="support@jzjdm.co", recipients=[""], text_body="body", html_body="html body"):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(id):
    user = User.get_user_by_id(id)
    token = get_reset_password_token(int(id))
    send_email('[JZ JDM] Reset Your Password',
            sender="support@jzjdm.co",
            recipients=[str(user.email)],
            text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
            html_body=render_template('email/reset_password.html',
                                        user=user, token=token))

@login.user_loader
def load_user(id):
    return User.get_user_by_id(id)

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = Search()
    if form.validate_on_submit():
        return redirect(url_for("listings", q=form.search_field.data))
    CAROUSEL_CARS = 5
    carousel_cars = Car.search_cars()[0:CAROUSEL_CARS]
    return render_template("index.html", carousel_cars=carousel_cars, form=form, title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.is_submitted() and form.validate(): #form.validate_on_submit():
        user = User.get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form, title="Login")

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
        User.add_user(User(form.username.data, form.email.data, form.password.data))
        flash("Congratulations, you are now a registered user!")
        refresh_database()
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="Register")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = User.get_user_by_id(current_user.get_id())
    form = ResetPassword()
    if form.validate_on_submit():
        user.change_password(form.password.data)
        flash("Password Successfully Changed")
        return redirect(url_for("profile"))
    update_email = UpdateEmail()
    if update_email.validate_on_submit():
        User.update_email(update_email.email.data, int(current_user.get_id()))
        flash("Email successfully updated")
        return redirect(url_for("profile"))
    cars = Car.get_favorited_cars_by_user_id(user.id)
    sender_ids = DirectMessage.get_sender_ids_of_user(int(current_user.get_id()))
    users = User.get_all_users()
    senders = [u for u in users if u.id in sender_ids]
    return render_template("profile.html", user=user, cars=cars, senders=senders, form=form, update_email=update_email, title="Profile")

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")

@app.route("/listings", methods=["GET", "POST"])
def listings():
    form = Search()
    if form.validate_on_submit():
        return redirect(url_for("listings", q=form.search_field.data))
    q = request.args.get("q", None)
    cars = Car.search_cars(q) 
    page = int(request.args.get("page", 1))
    offset = (page - 1) * Config.CARS_PER_PAGE
    amount = Config.CARS_PER_PAGE
    cars = cars[offset:offset+amount] 
    prev_url = None
    next_url = None
    if page > 1:
        prev_url = url_for("listings", page=(page-1), q=q)
    if len(cars) >= Config.CARS_PER_PAGE:
        next_url = url_for("listings", page=(page+1), q=q)
    return render_template("listings.html", form=form, cars=cars, prev_url=prev_url, next_url=next_url, q=q, title="View Cars")

@app.route("/car/<int:id>")
def car(id):
    car = Car.get_car_by_id(int(id))
    if not car:
        abort(404)
    images = car.get_images()
    images.sort(key=(lambda x: x.cover_img), reverse=True)
    cover_image = images[0]
    NUMBER_OF_SIMILAR_CARS = 6
    similar = Car.search_cars(car.query_from_car())[1:NUMBER_OF_SIMILAR_CARS+1]
    return render_template("car.html", car=car, similar=similar, images=images, cover_image=cover_image, title=f"{car.oem.title()}, {car.model.title()}")

@app.route("/loan")
def loan():
    price = request.args.get("price", None)
    return render_template("loan.html", price=price, title="Loan Calculator")

@app.route("/control", methods=["GET", "POST"])
@login_required
def control():
    users = User.get_all_users()
    if [u for u in users if int(u.id) == int(current_user.get_id())][0].super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = CarCreationForm()
    if form.validate_on_submit():
        car = Car(form.description.data, form.oem.data, form.model.data, form.year.data, form.mileage.data, form.color.data, form.price.data, form.drivetrain.data, form.engine_cylinder.data, form.engine_size.data, int(form.four_wheel_steering.data), int(form.abs.data), int(form.tcs.data), form.doors.data, form.seats.data, form.horsepower.data, form.torque.data, form.misc.data)
        Car.add_car(car)
        flash("Car added")
        refresh_database()
        return redirect(url_for("control"))
    cars = Car.get_all_cars()
    return render_template("control.html", form=form, cars=cars, users=users, title="Control Center")

@app.route("/control/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def configure_sales_rep(user_id):
    if User.get_user_by_id(current_user.get_id()).super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = ConfigureSalesRep()
    user = User.get_user_by_id(user_id)
    sales_rep = SalesRep.get_sales_rep_by_user_id(user_id)
    if form.validate_on_submit():
        if not sales_rep:
            SalesRep.add_sales_rep(SalesRep(user, form.about.data, form.image_link.data))
        else:
            if form.about.data:
                SalesRep.update_sales_rep_about(sales_rep, form.about.data)
            if form.image_link.data:
                SalesRep.update_sales_rep_image_link(sales_rep, form.image_link.data)
        flash("Sales Rep updated")
        return redirect(url_for('configure_sales_rep', user_id=user_id))
    cars = Car.get_cars_by_sales_rep_id(int(user.id))
    return render_template("salesRepControl.html", form=form, user=user, sales_rep=sales_rep, cars=cars)

@app.route("/control/users/<int:sales_rep_id>/assign")
@login_required
def assign_cars(sales_rep_id):
    if User.get_user_by_id(current_user.get_id()).super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    cars = Car.get_all_cars()
    cars = [c for c in cars if int(c.sales_rep_id) == -1]
    sales_rep = SalesRep.get_sales_rep_by_user_id(sales_rep_id)
    return render_template("assignCars.html", sales_rep=sales_rep, cars=cars)

@app.route("/control/cars/<int:car_id>", methods=["GET", "POST"])
@login_required
def add_image_to_car(car_id):
    if User.get_user_by_id(current_user.get_id()).super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = AddImages()
    if form.validate_on_submit():
        if form.image1.data:
            Image.add_image(Image(form.image1.data, car_id, int(form.cover_image.data)))
        image_data = [form.image2.data, form.image3.data, form.image4.data, form.image5.data, form.image6.data, form.image7.data, form.image8.data, form.image9.data, form.image10.data]
        for image in image_data:
            if image:
                Image.add_image(Image(image, car_id))
        flash("Images successfully added")
        return redirect(url_for("add_image_to_car", car_id=car_id))
    car = Car.get_car_by_id(car_id)
    images = car.get_images() or []
    return render_template("addImage.html", car=car, form=form, images=images)

@app.route("/sales")
def sales_representatives():
    sales_reps = SalesRep.get_all_sales_reps() or []
    return render_template("salesRepresentatives.html", sales_reps=sales_reps, title="Sale Representatives")

@app.route("/sales/<int:sales_rep_id>")
def individual_sales_representative(sales_rep_id):
    sales_rep = SalesRep.get_sales_rep_by_user_id(int(sales_rep_id))
    cars = Car.get_cars_by_sales_rep_id(sales_rep_id) or []
    return render_template("individualSalesRepresentative.html", sales_rep=sales_rep, cars=cars, title=sales_rep.user.username)

@app.route("/sales/message/<int:sales_rep_id>", methods=["GET", "POST"])
@login_required
def message_sales_rep(sales_rep_id):
    # try an auto refresh method thing
    user = User.get_user_by_id(sales_rep_id)
    form = DirectMessageForm()
    if form.validate_on_submit():
        DirectMessage.send_direct_message(int(current_user.get_id()), int(user.id), form.content.data)
        return redirect(url_for("message_sales_rep", sales_rep_id=sales_rep_id))
    messages = DirectMessage.get_messages(current_user.get_id(), sales_rep_id) + DirectMessage.get_messages(sales_rep_id, current_user.get_id())
    messages.sort(key=(lambda x: int(x.id)))
    return render_template("messages.html", form=form, user=user, messages=messages, title=f"Messaging: {user.username}")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = Contact()
    if form.validate_on_submit():
        ContactMessage.add_message(ContactMessage(form.message.data, form.email.data))
        flash("Message Successfully Sent")
        return redirect(url_for("contact"))
    return render_template("contactUs.html", form=form, title="Contact Us")

@app.route("/owners")
def owners():
    return render_template("owners.html", title="Owners")

@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html", title="Accessibility")

@app.route("/reset", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("login"))
    form = ResetPasswordEmail()
    if form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        if not user:
            raise abort(500)
        send_password_reset_email(int(user.id))
        flash("Check your email!")
        return redirect(url_for("reset_password"))
    return render_template("resetPassword.html", form=form)

@app.route("/reset/password/<token>", methods=["GET", "POST"])
def change_from_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = verify_reset_password_token(token)
    if not user:
        flash("Invalid Token")
        return redirect(url_for("reset_password"))
    form = ResetPassword()
    if form.validate_on_submit():
        user.change_password(form.password.data)
        flash("Your password has been reset")
        return redirect(url_for("login"))
    return render_template("resetPasswordToken.html", form=form, user=user)

@app.route("/Privacy-Policy")
def privacyPolicy():
    return render_template("privacyPolicy.html", title="Privacy Policy")

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", title="PAGE NOT FOUND"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html", title="INTERNAL SERVER ERROR"), 500

# API
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/api/test", methods=["POST"])
def test():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 403)
    user = User.get_by_id(int(current_user.get_id()))
    if user is None or user.super_user == 0:
        return failure_response("You do not have the required privileges", 403)
    body = json.loads(request.data)
    value = body.get("value")
    print(f"it worked {value}")
    return success_response({"message": "hello"})

@app.route("/api/assign", methods=["POST"])
def assign_car_to_sales_rep():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 401)
    user = User.get_user_by_id(int(current_user.get_id()))
    if user is None or user.super_user == 0:
        return failure_response("You do not have the required privileges", 403)
    body = json.loads(request.data)
    car_id = int(body.get("carId"))
    user_id = int(body.get("userId"))
    if not SalesRep.is_user_id_a_sales_rep(user_id):
        return failure_response(f"id {user_id} is not a sales rep", 400)
    Car.assign_sales_rep(car_id, user_id)
    return success_response({}, 201)

@app.route("/api/flash", methods=["POST"])
def demo_flash():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 401)
    user = User.get_user_by_id(int(current_user.get_id()))
    if user is None or user.super_user == 0:
        return failure_response("You do not have the required privileges", 403)
    flash("This is a flashed message for styling")
    return success_response({})

@app.route("/api/favorite", methods=["POST"])
def favorite_car():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 401)
    body = json.loads(request.data)
    user_id = int(current_user.get_id())
    car_id = int(body.get("car_id", -1))
    User.favorite_car(user_id, car_id)
    return success_response({})

@app.route("/api/unfavorite", methods=["POST"])
def unfavorite_car():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 401)
    body = json.loads(request.data)
    user_id = int(current_user.get_id())
    car_id = int(body.get("car_id", -1))
    User.remove_favorite(user_id, car_id)
    return success_response({})

@app.route("/api/messages", methods=["POST"])
def get_messages():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 401)
    body = json.loads(request.data)
    user_id = int(current_user.get_id())
    recipient_id = int(body.get("recipient_id", -1))
    messages = DirectDatabaseDirectMessage.get_messages(user_id, recipient_id) + DirectDatabaseDirectMessage.get_messages(recipient_id, user_id)
    messages.sort(key=(lambda x: int(x.id)))
    return success_response({"messages": [message.__dict__ for message in messages]})

@app.route("/api/id", methods=["POST"])
def get_user_id():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 401)
    return success_response({"user_id": int(current_user.get_id())})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

