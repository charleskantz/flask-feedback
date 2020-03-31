from flask import Flask, redirect, render_template, session, abort
from models import db, connect_db, User, add_user_to_db, Feedback, add_feedback_to_db
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUser, LoginUser, AddFeedback

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

        return redirect(f"/users/{user.username}")

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
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Incorrect username/password"]
    else:
        return render_template("login.html", form=form)


@app.route("/users/<username>")
def get_secret(username):
    """ shows our user's detail page and feedback """

#  how do we address the keyerror if session is empty (no one logged in)
    if session["username"] == username:
        current_user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=username).all()

        return render_template("secret.html", user=current_user,
                               feedback=feedback)
    else:

        return abort(401, description="you don't have access to this page.")


@app.route("/logout")
def logout_user():

    session.pop("username")
    return redirect("/")


@app.route("/users/<username>/delete")
def delete_user(username):
    """ deletes user from db """
    if session["username"] == username:
        # deletes user feedback
        user_feedback = Feedback.query.get_or_404(username=username).all()
        db.session.delete(user_feedback)
        # deletes user
        current_user = User.query.get_or_404(username=username)
        db.session.delete(current_user)

        db.session.commit()
        return redirect("/")
    else:
        return abort(401, description="you don't have access to this operation.")


@app.route("/users/<username>/feedback/add", methods=["POST", "GET"])
def access_feedback_form(username):
    if session["username"] != username:
        return abort(401, description="You  don't have access to this page.")
    else:
        form = AddFeedback()
        existing_user = User.query.all()
        print("\n\n\n THIS IS OUR EXISTING USER\n\n\n", existing_user)
        user_list = [(u.username, u.username) for u in existing_user]
        form.username.choices = user_list

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            username = form.username.data

            new_feedback = Feedback(title=title,
                                    content=content,
                                    username=username)
            add_feedback_to_db(new_feedback)
            return redirect(f'/users/{username}')

        else:
            return render_template("addfeedback.html", form=form)
