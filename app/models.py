from app import db

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

class User(db.Model):
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