from app import db
from flask_login import UserMixin

'''
we have 2 model classes - User and Review
one user can have multiple reviews
therefore, a user shares one to many relationship with review
__tablename__ = users
__tablename__ = reviews

update:
since our application will allow users to comment on posts,
we will create another table to hold the comments
__tablename__ = 'comments'
this table will have 2 foreign keys, one pointing to the user who created the comment
and the other to the post which has been commented on
'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

'''
the User class will also inherit from UserMixin class
this class attaches 4 methods

Flask-login requires a User model with the following properties:

    has an is_authenticated() method that returns True if the user has provided
    valid credentials
    has an is_active() method that returns True if the user’s account is active
    has an is_anonymous() method that returns True if the current user is an anonymous user
    has a get_id() method which, given a User instance, returns the unique ID for that object

UserMixin class provides the implementation of this properties.
Its the reason you can call for example is_authenticated to check if login
credentials provide is correct or not instead of having to write a method to do that yourself.

'''
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    '''
    backref is a simple way to declare a new property on the Review class
    you can then also use Review.user to get the reviews of that user
    lazy defines when sqlalchemy will load the data from the database
    '''
    reviews = db.relationship('Review', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    '''
    tags will actually be a list, but since we can't store lists in the database,
    we will serialize it and store it as a string and when we retrieve, we will
    deserialize it into a list
    '''
    tags = db.Column(db.String(200), nullable=False)
    upvotes = db.Column(db.Integer, nullable=False)
    downvotes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='review', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('reviews.id'))