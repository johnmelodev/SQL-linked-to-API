from flask import Flask, jsonify, request, make_response
from database_structure import Author, Post, app, db
import json
import jwt
from datetime import datetime, timedelta
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if a token was sent
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token not included!'}, 401)
        # If we have a token, validate access by querying the DB
        try:
            result = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            author = Author.query.filter_by(
                id_author=result['id_author']).first()
        except:
            return jsonify({'message': 'Token is invalid'}, 401)
        return f(author, *args, **kwargs)
    return decorated

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Invalid login', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    user = Author.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Invalid login', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    if auth.password == user.password:
        token = jwt.encode({'id_author': user.id_author, 'exp': datetime.utcnow(
        ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Invalid login', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/')
@token_required
def get_posts(author):
    posts = Post.query.all()

    list_posts = []
    for post in posts:
        current_post = {}
        current_post['title'] = post.title
        current_post['id_author'] = post.id_author
        list_posts.append(current_post)
    return jsonify({'posts': list_posts})

# Get post by id - GET https://localhost:5000/post/1

@app.route('/post/<int:id_post>', methods=['GET'])
@token_required
def get_post_by_id(author, id_post):
    post = Post.query.filter_by(id_post=id_post).first()
    current_post = {}
    try:
        current_post['title'] = post.title
    except:
        pass
    current_post['id_author'] = post.id_author

    return jsonify({'posts': current_post})

# Create a new post - POST https://localhost:5000/post

@app.route('/post', methods=['POST'])
@token_required
def new_post(author):
    new_post = request.get_json()
    post = Post(
        title=new_post['title'], id_author=new_post['id_author'])

    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'})

# Modify an existing post - PUT https://localhost:5000/post/1

@app.route('/post/<int:id_post>', methods=['PUT'])
@token_required
def edit_post(author, id_post):
    edited_post = request.get_json()
    post = Post.query.filter_by(id_post=id_post).first()
    try:
        post.title = edited_post['title']
    except:
        pass
    try:
        post.id_author = edited_post['id_author']
    except:
        pass

    db.session.commit()
    return jsonify({'message': 'Post edited successfully'})

# Delete a post - DELETE - https://localhost:5000/post/1

@app.route('/post/<int:id_post>', methods=['DELETE'])
@token_required
def delete_post(author, id_post):
    post_to_delete = Post.query.filter_by(
        id_post=id_post).first()
    if not post_to_delete:
        return jsonify({'message': 'No post found with this id'})
    db.session.delete(post_to_delete)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'})

@app.route('/authors')
@token_required
def get_authors(author):
    authors = Author.query.all()
    authors_list = []
    for a in authors:
        current_author = {}
        current_author['id_author'] = a.id_author
        current_author['name'] = a.name
        current_author['email'] = a.email
        authors_list.append(current_author)

    return jsonify({'authors': authors_list})

@app.route('/authors/<int:id_author>', methods=['GET'])
@token_required
def get_author_by_id(author, id_author):
    author = Author.query.filter_by(id_author=id_author).first()
    if not author:
        return jsonify('Author not found!')
    current_author = {}
    current_author['id_author'] = author.id_author
    current_author['name'] = author.name
    current_author['email'] = author.email

    return jsonify({'author': current_author})

# Create a new author

@app.route('/authors', methods=['POST'])
@token_required
def new_author(author):
    new_author_data = request.get_json()
    author = Author(
        name=new_author_data['name'], password=new_author_data['password'], email=new_author_data['email'])

    db.session.add(author)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}, 200)

@ app.route('/authors/<int:id_author>', methods=['PUT'])
@token_required
def edit_author(author, id_author):
    user_to_edit = request.get_json()
    author = Author.query.filter_by(id_author=id_author).first()
    if not author:
        return jsonify({'Message': 'This user was not found'})
    try:
        author.name = user_to_edit['name']
    except:
        pass
    try:
        author.email = user_to_edit['email']
    except:
        pass
    try:
        author.password = user_to_edit['password']
    except:
        pass

    db.session.commit()
    return jsonify({'message': 'User edited successfully'})

@ app.route('/authors/<int:id_author>', methods=['DELETE'])
@token_required
def delete_author(author, id_author):
    existing_author = Author.query.filter_by(id_author=id_author).first()
    if not existing_author:
        return jsonify({'message': 'This author was not found'})
    db.session.delete(existing_author)
    db.session.commit()

    return jsonify({'message': 'Author deleted successfully'})

app.run(port=5050, host='localhost', debug=True)
