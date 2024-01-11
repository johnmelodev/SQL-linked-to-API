from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a Flask API
app = Flask(__name__)
# Create an instance of SQLAlchemy
app.config['SECRET_KEY'] = 'FSD2323f#$!SAH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
db: SQLAlchemy

# Define the structure of the Post table: id_post, title, author

class Post(db.Model):
    __tablename__ = 'post'
    id_post = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    id_author = db.Column(db.Integer, db.ForeignKey('author.id_author'))

# Define the structure of the Author table: id_author, name, email, password, admin, posts

class Author(db.Model):
    __tablename__ = 'author'
    id_author = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)
    posts = db.relationship('Post')

# Execute the command to create the database
with app.app_context():
    db.drop_all()
    db.create_all()
    # Create admin users
    author = Author(name='john', email='john@email.com',
                  password='123456', admin=True)
    db.session.add(author)
    db.session.commit()
