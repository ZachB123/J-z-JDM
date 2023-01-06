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


