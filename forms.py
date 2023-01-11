from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.get_by_username(username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')

class CarCreationForm(FlaskForm):
    description = TextAreaField("Description")
    oem = StringField("O.E.M")
    model = StringField("Model")
    year = IntegerField("Year:int")
    mileage = IntegerField("Mileage:int")
    color = StringField("Color")
    price = IntegerField("Price:int")
    drivetrain = StringField("Drivetrain")
    engine_cylinder = StringField("Engine Cylinder")
    engine_size = IntegerField("Engine Size:int")
    four_wheel_steering = BooleanField("Four Wheel Steering")
    abs = BooleanField("ABS")
    tcs = BooleanField("TCS")
    doors = IntegerField("Doors:int")
    seats = IntegerField("Seats:int")
    horsepower = IntegerField("Horsepower:int")
    torque = IntegerField("Torque:int")
    misc = TextAreaField("Misc")
    submit = SubmitField("Add Car. Please double check all the form entries. Zach does not want to manually fix stuff")

class AddImages(FlaskForm):
    image1 = StringField("Image1", validators=[DataRequired()])
    cover_image = BooleanField("Is image1 the cover image?")
    image2 = StringField("Image2")
    image3 = StringField("Image3")
    image4 = StringField("Image4")
    image5 = StringField("Image5")
    image6 = StringField("Image6")
    image7 = StringField("Image7")
    image8 = StringField("Image8")
    image9 = StringField("Image9")
    image10 = StringField("Image10")
    submit = SubmitField("Add images")

class ConfigureSalesRep(FlaskForm):
    about = TextAreaField("about")
    image_link = StringField("image_link")
    submit = SubmitField("submit")

class Contact(FlaskForm):
    name = StringField("Name")
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")



