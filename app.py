from flask import Flask, redirect, render_template, session
from models import db, connect_db, User, add_user_to_db
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUser, LoginUser

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
        user = User.register_user(form)

        add_user_to_db(user)

        return redirect("/secret")

    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def handle_login():
    """ handles user login """
    form = LoginUser()


    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        authentication = User.log_in_user(form)
        if authentication:
            session["username"] = username
            return redirect("/secret")
        else:
            form.username.errors = ["Incorrect username/password"]
    else:
        return render_template("login.html", form=form)

@app.route("/secret")
def get_secret():
    return render_template("secret.html")
