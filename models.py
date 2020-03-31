from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User class """

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register_user(cls, form):
        username = form.username.data
        pwd = form.password.data
        hashed = bcrypt.generate_password_hash(pwd)

        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username,
                   password=hashed_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    @classmethod
    def log_in_user(cls, form):
        username = form.username.data
        submitted_pw = form.password.data
        current_user = User.query.filter_by(username=username).first()

        if current_user and bcrypt.check_password_hash(current_user.password,
                                                       password=submitted_pw):
            return current_user
        else:
            return False


def add_user_to_db(user):
    """ takes user data and submits to DB """

    db.session.add(user)
    db.session.commit()
    return flash(f'{user.username} added!')


# TODO: make helper function to Bcrypt / has the PW

class Feedback(db.Model):
    """ feedback model """

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"))

def add_feedback_to_db(feedback):
    db.session.add(feedback)
    db.session.commit()
    return flash(f'{feedback.title} added!')


