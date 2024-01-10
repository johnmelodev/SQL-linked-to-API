from flask import Flask, jsonify, request

app = Flask(__name__)

posts = [
    {
        'title': 'My Story',
        'author': 'Amanda Dias'
    },
    {
        'title': 'New Sony Device',
        'author': 'Howard Stringer'
    },
    {
        'title': 'Launch of the Year',
        'author': 'Jeff Bezos'
    }
]

# Default route - GET http://localhost:5010


@app.route('/')
def get_posts():
    return jsonify(posts)

# Get with Id - GET http://localhost:5010/post/1


@app.route('/post/<int:index>', methods=['GET'])
def get_post_by_index(index):
    return jsonify(posts[index])

# Create a new post - POST http://localhost:5010/post


@app.route('/post', methods=['POST'])
def new_post():
    post = request.get_json()
    posts.append(post)

    return jsonify(post, 200)

# Modify an existing post - PUT http://localhost:5010/post/<int:index>


@app.route('/post/<int:index>', methods=['PUT'])
def modify_post(index):
    modified_post = request.get_json()
    posts[index].update(modified_post)

    return jsonify(posts[index], 200)

# Delete a post - DELETE http://localhost:5010/post/1


@app.route('/post/<int:index>', methods=['DELETE'])
def delete_post(index):
    if posts[index] is not None:
        deleted_post = posts.pop(index)
        return jsonify(f'The post {deleted_post} has been deleted', 200)
    return jsonify('Could not find the post for deletion', 404)


app.run(port=5010, host='localhost', debug=True)
