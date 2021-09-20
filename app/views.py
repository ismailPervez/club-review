from app import app
from flask import render_template, redirect, url_for, request
from app.forms import RegistrationForm, LoginForm, CreatePitchForm, CommentForm
from app.models import Comment, Review, User
from app import db, bcrypt

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