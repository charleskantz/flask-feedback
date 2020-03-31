from flask import Flask, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUser

API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
db.create_all()
debug = DebugToolbarExtension(app)


@app.route('/')
def redirect_to_register():
    """ redirect to '/register' """

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """ form to register user """

    form = RegisterUser()

    if form.validate_on_submit():


        return redirect("/")

    else:
        return render_template("register.html", form=form)
