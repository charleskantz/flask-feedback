from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email


class RegisterUser(FlaskForm):
    """ form to register a user """

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class LoginUser(FlaskForm):
    """ form to log in  user """
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class AddFeedback(FlaskForm):
    title = StringField("Title:", validators=[InputRequired()])
    content = StringField("Content:", validators=[InputRequired()])
    #dynamic selection using list  comprehension
    username = SelectField("Users:",validators=[InputRequired()] )
