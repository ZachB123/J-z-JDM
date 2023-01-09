import os
from config import Config
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from dotenv import load_dotenv
load_dotenv()
from forms import LoginForm, RegistrationForm, CarCreationForm, AddImages, ConfigureSalesRep, Contact
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import User, Car, Image, SalesRep, Message
from werkzeug.urls import url_parse

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
        User.add_user(User(form.username.data, form.email.data, form.password.data))
        flash("Congratulations, you are now a registered user!")
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
    page = int(request.args.get("page", 1))
    prev_url = None
    next_url = None
    if page > 1:
        prev_url = url_for("listings", page=(page-1))
    cars = Car.paginate_cars(page)
    if len(cars) >= Config.CARS_PER_PAGE:
        next_url = url_for("listings", page=(page+1))
    return render_template("listings.html", cars=cars, prev_url=prev_url, next_url=next_url)

@app.route("/car/<int:id>")
def car(id):
    car = Car.get_car_by_id(id)
    if not car:
        abort(404)
    return render_template("car.html", car=car)

@app.route("/loan")
def loan():
    return render_template("loan.html")

@app.route("/control", methods=["GET", "POST"])
@login_required
def control():
    if User.get_by_id(int(current_user.get_id())).super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = CarCreationForm()
    if form.validate_on_submit():
        car = Car(form.description.data, form.oem.data, form.model.data, form.year.data, form.mileage.data, form.color.data, form.price.data, form.drivetrain.data, form.engine_cylinder.data, form.engine_size.data, int(form.four_wheel_steering.data), int(form.abs.data), int(form.tcs.data), form.doors.data, form.seats.data, form.horsepower.data, form.torque.data, form.misc.data)
        Car.add_car(car)
        flash("Car added")
        return redirect(url_for("control"))
    cars = Car.get_all_cars()
    users = User.get_all_users()
    return render_template("control.html", form=form, cars=cars, users=users)

@app.route("/control/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def configure_sales_rep(user_id):
    if User.get_by_id(int(current_user.get_id())).super_user == 0:
        flash("You do not have the required privileges to view this page")
        return redirect(url_for("index"))
    form = ConfigureSalesRep()
    user = User.get_by_id(user_id)
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
    return render_template("salesRepControl.html", form=form, user=user, sales_rep=sales_rep)

@app.route("/control/cars/<int:car_id>", methods=["GET", "POST"])
@login_required
def add_image_to_car(car_id):
    if User.get_by_id(int(current_user.get_id())).super_user == 0:
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
    car = Car.get_car_by_id(car_id)
    images = car.get_images() or []
    return render_template("addImage.html", car=car, form=form, images=images)

@app.route("/sales")
def sales_representatives():
    sales_reps = SalesRep.get_all_sales_reps() or []
    return render_template("salesRepresentatives.html", sales_reps=sales_reps)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = Contact()
    if form.validate_on_submit():
        Message.add_message(Message(form.message.data, form.name.data))
        flash("Message Successfully Sent")
    return render_template("contactUs.html", form=form)

@app.route("/Accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/Privacy-Policy")
def privacyPolicy():
    return render_template("privacyPolicy.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

