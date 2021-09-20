from app import app
from flask import render_template, redirect, url_for, request
from app.forms import RegistrationForm, LoginForm, CreatePitchForm, CommentForm
from app.models import Comment, Review, User
from app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

# routes
@app.route("/")
def home():
    return render_template('index.html')

# sign up page
@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    form  = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed_password
        )

        db.session.add(user)
        db.session.commit()

        print("account created successfully!")
        return redirect(url_for('home')) # you pass in the view function name and not the 
        # route name
    else:
        print('account NOT created')
    return render_template('register.html', form=form)

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # check if the url has a parameter - next
            next_route = request.args.get('next')
            login_user(user)
            print("successfully logged in as: ", current_user.username)
            return redirect(next_route) if next_route else redirect(url_for('home'))


    return render_template("login.html", form=form)