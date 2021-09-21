from app import app
from flask import render_template, redirect, url_for, request
from app.forms import RegistrationForm, LoginForm, CreatePitchForm, CommentForm
from app.models import Comment, Review, User
from app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import ast

# routes
@app.route("/")
def home():
    reviews = Review.query.order_by(Review.id.desc()).limit(3).all()
    latest_reviews = []
    users = []
    for review in reviews:

        user = User.query.filter_by(id=review.user_id).first()
        users.append(user)

        review = Review(
            id=review.id,
            title=review.title,
            content=review.content,
            upvotes=review.upvotes,
            downvotes=review.downvotes,
            tags=review.tags,
            user_id=review.user_id
        )
        review.tags = ast.literal_eval(review.tags)
        latest_reviews.append(review)

    # get job pitches
    job_reviews = Review.query.order_by(Review.id.desc()).limit(15).all()
    print(job_reviews)

    latest_job_reviews = []
    job_reviews_users = []
    for review in job_reviews:
        review = Review(
            id=review.id,
            title=review.title,
            content=review.content,
            upvotes=review.upvotes,
            downvotes=review.downvotes,
            tags=review.tags,
            user_id=review.user_id
        )
        review.tags = ast.literal_eval(review.tags)
        print(review.tags)

        if 'jobpitch' in review.tags or 'interviewpitch' in review.tags:
            print('its a job pitch')
            latest_job_reviews.append(review)
            user = User.query.filter_by(id=review.user_id).first()
            job_reviews_users.append(user)

    if len(latest_job_reviews) > 3:
        latest_job_reviews = latest_job_reviews[:3]
        job_reviews_users = job_reviews_users[:3]
    # print(latest_job_reviews)
    # print(job_reviews_users)

    return render_template('index.html', latest_reviews=latest_reviews, users=users, latest_job_reviews=latest_job_reviews, job_reviews_users=job_reviews_users)

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

# route for logging out user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# create post route
@app.route("/create", methods=["GET", "POST"])
def create():
    form = CreatePitchForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # the tags need to be JSON serializable before we store them in the database
        tags = form.tags.data.split(' ')
        # initial upvotes and downvotes are 0
        review = Review(
            title=title,
            content=content,
            tags=str(tags),
            upvotes=0,
            downvotes=0,
            user_id=current_user.id
        )

        db.session.add(review)
        db.session.commit()

        print('form submitted successfully!')

        return redirect(url_for("account"))

    else:
        print('not validated')

    # review = Review(, ,)

    return render_template("createpost.html", form=form)