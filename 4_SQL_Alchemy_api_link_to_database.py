# pip3 install flask-sqlalchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a Flask API
app = Flask(__name__)

# Create an instance of SQLAlchemy
app.config['SECRET_KEY'] = 'FSD2323f#$!SAH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'


# Initialize SQLAlchemy
db = SQLAlchemy(app)
db: SQLAlchemy

# post_id, title, author_id


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))

# Define the structure of the author table
# author_id, name, email, password, admin, posts


class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)
    posts = db.relationship('Post')


with app.app_context():
    # Execute the command to create the database

    db.drop_all()
    db.create_all()

    # Create admin users

    # Create an instance of the Author class
    author = Author(name='John', email='john@email.com',
                    password='123456', admin=True)
    # Add the instance to the database
    db.session.add(author)
    # Commit the changes to the database
    db.session.commit()
