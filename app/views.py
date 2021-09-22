from app import app, db, bcrypt, mail
from flask import render_template, redirect, url_for, request
from app.forms import RegistrationForm, LoginForm, CreatePitchForm, CommentForm
from app.models import Comment, Review, User
from flask_login import login_user, current_user, logout_user, login_required
import ast
from flask_mail import Message

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

        msg = Message("welcome to club review", sender="noreply@clubreview.com", recipients=[form.email.data])
        msg.body = f'''
            welcome to club review
            Hi {form.username.data},
            welcome to club review. thanks for joining our ever growing society
        '''
        
        mail.send(msg)
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

'''
user acccount
'''
@app.route('/account')
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first()
    all_reviews = user.reviews
    
    total_upvote_count = 0
    total_downvote_count = 0
    for review in all_reviews:
        # this method converts a string representation of a list into a list
        review.tags = ast.literal_eval(review.tags)
        total_upvote_count += review.upvotes
        total_downvote_count += review.downvotes

    print(total_upvote_count)
    print(total_downvote_count)

    return render_template('account.html', reviews=all_reviews, upvotes=total_upvote_count, downvotes=total_downvote_count)


'''
make a view to delete each post
'''
@app.route('/delete/<int:post_id>', methods=["GET", "DELETE"])
def delete_post(post_id):
    # check if the post belongs to the current user before deleting it
    post = Review.query.filter_by(id=post_id).first()
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('account'))


# update a review/post - when liked or disliked
@app.route('/update/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    review = Review.query.filter_by(id=post_id).first()
    if "upvotes" in request.json:
        review.upvotes = request.json["upvotes"]

    if "downvotes" in request.json:
        review.downvotes = request.json["downvotes"]

    db.session.commit()

    return "status: ok"


# full post
@app.route("/full-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def full_post(post_id):
    form = CommentForm()
    review = Review.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=review.user_id).first()
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

    # all comments for this post
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    users = []
    for comment in comments:
        user = User.query.filter_by(id=comment.user_id).first()
        users.append(user)

    print(comments)

    if form.validate_on_submit():
        comment = form.content.data
        comment = Comment(content=comment, user_id=current_user.id, post_id=post_id)

        db.session.add(comment)
        db.session.commit()

    return render_template("fullpost.html", form=form, post=review, user=user, comments=comments, users=users)