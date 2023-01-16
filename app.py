import os
from config import Config
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from dotenv import load_dotenv
load_dotenv()
from forms import LoginForm, RegistrationForm, CarCreationForm, AddImages, ConfigureSalesRep, Contact, DirectMessageForm, Search
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import User, Car, Image, SalesRep, Message, DirectMessage
from werkzeug.urls import url_parse
# from flask_caching import Cache
from diskcache import Cache
import threading
import time
import json

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "login"
# cache = Cache(app)
cache = Cache(".cache", statistic=True)

# cache.set("CAR_CACHE", Car.get_all_cars())
# cache.set("USER_CACHE", User.get_all_users())
cache.add("CAR_CACHE", Car.get_all_cars())
cache.add("USER_CACHE", User.get_all_users())


@login.user_loader
def load_user(id):
    return User.get_by_id(id)
    # USER_CACHE = cache.get("USER_CACHE")
    # return [u for u in USER_CACHE if int(u.id) == int(id)][0]

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
        USER_CACHE = cache.get("USER_CACHE")
        user = [u for u in USER_CACHE if u.username == form.username.data][0]
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
        User.add_user(User(form.username.data, form.email.data, form.password.data))
        cache.add("USER_CACHE", User.get_all_users())
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/profile")
@login_required
def profile():
    USER_CACHE = cache.get("USER_CACHE")
    user = [u for u in USER_CACHE if int(u.id) == int(current_user.get_id())][0]
    cars = Car.get_favorited_cars_by_user_id(user.id)
    return render_template("profile.html", user=user, cars=cars)

@app.route("/company")
def company():
    return render_template("company.html")

@app.route("/listings", methods=["GET", "POST"])
def listings():
    form = Search()
    print("form")
    if form.validate_on_submit():
        return redirect(url_for("listings", q=form.search_field.data))
    page = int(request.args.get("page", 1))
    print("page")
    q = request.args.get("q", None)
    prev_url = None
    next_url = None
    if page > 1:
        prev_url = url_for("listings", page=(page-1))
    print("before cars")
    cars = Car.search_cars(q) #cache.get("CAR_CACHE")
    print("after cars")
    offset = (page - 1) * Config.CARS_PER_PAGE
    amount = Config.CARS_PER_PAGE
    cars = cars[offset:offset+amount] 
    print("offset")
    if len(cars) >= Config.CARS_PER_PAGE:
        next_url = url_for("listings", page=(page+1), q=q)
    print("about to render")
    return render_template("listings.html", form=form, cars=cars, prev_url=prev_url, next_url=next_url, q=q)

@app.route("/car/<int:id>")
def car(id):
    CAR_CACHE = cache.get("CAR_CACHE")
    car = [i for i in CAR_CACHE if int(i.id) == id]
    if not car:
        abort(404)
    car = car[0]
    return render_template("car.html", car=car)

@app.route("/loan")
def loan():
    price = request.args.get("price", None)
    return render_template("loan.html", price=price)

@app.route("/control", methods=["GET", "POST"])
@login_required
def control():
    USER_CACHE = cache.get("USER_CACHE")
    if [u for u in USER_CACHE if int(u.id) == int(current_user.get_id())][0].super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = CarCreationForm()
    if form.validate_on_submit():
        car = Car(form.description.data, form.oem.data, form.model.data, form.year.data, form.mileage.data, form.color.data, form.price.data, form.drivetrain.data, form.engine_cylinder.data, form.engine_size.data, int(form.four_wheel_steering.data), int(form.abs.data), int(form.tcs.data), form.doors.data, form.seats.data, form.horsepower.data, form.torque.data, form.misc.data)
        Car.add_car(car)
        cache.add("CAR_CACHE", Car.get_all_cars())
        flash("Car added")
        return redirect(url_for("control"))
    cars = cache.get("CAR_CACHE")
    users = USER_CACHE
    return render_template("control.html", form=form, cars=cars, users=users)

@app.route("/control/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def configure_sales_rep(user_id):
    USER_CACHE = cache.get("USER_CACHE")
    if [u for u in USER_CACHE if int(u.id) == int(current_user.get_id())][0].super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = ConfigureSalesRep()
    user = [u for u in USER_CACHE if int(u.id) == int(user_id)][0]
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
    USER_CACHE = cache.get("USER_CACHE")
    if [u for u in USER_CACHE if int(u.id) == int(current_user.get_id())][0].super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    cars = cache.get("CAR_CACHE")
    cars = [c for c in cars if int(c.sales_rep_id) == -1]
    sales_rep = SalesRep.get_sales_rep_by_user_id(sales_rep_id)
    cache.add("CAR_CACHE", Car.get_all_cars())
    return render_template("assignCars.html", sales_rep=sales_rep, cars=cars)

@app.route("/control/cars/<int:car_id>", methods=["GET", "POST"])
@login_required
def add_image_to_car(car_id):
    USER_CACHE = cache.get("USER_CACHE")
    if [u for u in USER_CACHE if int(u.id) == int(current_user.get_id())][0].super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = AddImages()
    if form.validate_on_submit():
        if form.image1.data:
            Image.add_image(Image(form.image1.data, car_id, int(form.cover_image.data)))
        if form.image2.data:
            Image.add_image(Image(form.image2.data, car_id))
        if form.image3.data:
            Image.add_image(Image(form.image3.data, car_id))
        if form.image4.data:
            Image.add_image(Image(form.image4.data, car_id))
        if form.image5.data:
            Image.add_image(Image(form.image5.data, car_id))
        if form.image6.data:
            Image.add_image(Image(form.image6.data, car_id))
        if form.image7.data:
            Image.add_image(Image(form.image7.data, car_id))
        if form.image8.data:
            Image.add_image(Image(form.image8.data, car_id))
        if form.image9.data:
            Image.add_image(Image(form.image9.data, car_id))
        if form.image10.data:
            Image.add_image(Image(form.image10.data, car_id))
        flash("Images successfully added")
        return redirect(url_for("add_image_to_car", car_id=car_id))
    CAR_CACHE = cache.get("CAR_CACHE")
    car = [i for i in CAR_CACHE if int(i.id) == int(car_id)][0]
    images = car.get_images() or []
    return render_template("addImage.html", car=car, form=form, images=images)

@app.route("/sales")
def sales_representatives():
    sales_reps = SalesRep.get_all_sales_reps() or []
    return render_template("salesRepresentatives.html", sales_reps=sales_reps)

@app.route("/sales/<int:sales_rep_id>")
def individual_sales_representative(sales_rep_id):
    sales_rep = SalesRep.get_sales_rep_by_user_id(int(sales_rep_id))
    cars = Car.get_cars_by_sales_rep_id(sales_rep_id) or []
    return render_template("individualSalesRepresentative.html", sales_rep=sales_rep, cars=cars)

@app.route("/sales/message/<int:sales_rep_id>", methods=["GET", "POST"])
@login_required
def message_sales_rep(sales_rep_id):
    # try an auto refrech method thing
    user = User.get_by_id(sales_rep_id)
    form = DirectMessageForm()
    if form.validate_on_submit():
        DirectMessage.send_direct_message(int(current_user.get_id()), int(user.id), form.content.data)
        return redirect(url_for("message_sales_rep", sales_rep_id=sales_rep_id))
    messages = DirectMessage.get_messages(current_user.get_id(), sales_rep_id) + DirectMessage.get_messages(sales_rep_id, current_user.get_id())
    messages.sort(key=(lambda x: x.timestamp))
    
    print(type(current_user.get_id()))
    return render_template("message.html", form=form, user=user, messages=messages)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = Contact()
    if form.validate_on_submit():
        Message.add_message(Message(form.message.data, form.name.data))
        flash("Message Successfully Sent")
        return redirect(url_for("contact"))
    return render_template("contactUs.html", form=form)

@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/Privacy-Policy")
def privacyPolicy():
    return render_template("privacyPolicy.html")

@app.before_first_request
def on_load():
    def refresh_caches():
        while True:
            cache.add("USER_CACHE", User.get_all_users())
            cache.add("CAR_CACHE", Car.get_all_cars())
            time.sleep(20)
    thread = threading.Thread(target=refresh_caches)
    thread.start()

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

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
    user = User.get_by_id(int(current_user.get_id()))
    if user is None or user.super_user == 0:
        return failure_response("You do not have the required privileges", 403)
    body = json.loads(request.data)
    car_id = int(body.get("carId"))
    user_id = int(body.get("userId"))
    if not SalesRep.is_user_id_a_sales_rep(user_id):
        return failure_response(f"id {user_id} is not a sales rep", 400)
    Car.assign_sales_rep(car_id, user_id)
    cache.add("CAR_CACHE", Car.get_all_cars())
    return success_response({}, 201)

@app.route("/api/flash", methods=["POST"])
def demo_flash():
    if current_user.is_anonymous:
        return failure_response("User is not logged in", 401)
    user = User.get_by_id(int(current_user.get_id()))
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
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

