from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_password(self, password):
        user = User.get_user_by_username(self.username.data)
        if user is None:
            raise ValidationError("Username does not exist")
        if not user.check_password(self.password.data):
            raise ValidationError("Incorrect Password")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField('Email (optional)', render_kw={"placeholder": "Email (used to reset password)"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired()], render_kw={"placeholder": "Repeat Password"})
    submit = SubmitField('Register')

    def validate_password2(self, password2):
        if not password2.data == self.password.data:
            raise ValidationError("Passwords Do Not Match")

    def validate_username(self, username):
        user = User.get_user_by_username(username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired()], render_kw={"placeholder": "Repeat Password"})
    submit = SubmitField("Submit")

    def validate_password2(self, password2):
        if not password2.data == self.password.data:
            raise ValidationError("Passwords Do Not Match")
        
class ResetPasswordEmail(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        if not User.email_exists(email.data):
            raise ValidationError("Email is not in database, try a different email or contact us through the contact us page.")


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
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")

class DirectMessageForm(FlaskForm):
    content = TextAreaField("Message", validators=[DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField("Send")

class Search(FlaskForm):
    search_field = StringField("Search", validators=[DataRequired()], render_kw={"placeholder": "Search"})
    submito = SubmitField("Search")

class EmptyForm(FlaskForm):
    submit = SubmitField("")