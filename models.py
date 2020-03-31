from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

def register_user_to_db(form):
    """ takes form data and submits to DB """

    username = form.data.username.data
    password = form.data.username.data
    email = form.data.username.data
    first_name = form.data.username.data
    last_name = form.data.username.data


# TODO: make helper function to Bcrypt / has the PW