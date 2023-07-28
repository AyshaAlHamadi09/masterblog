from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "entered from codio", "content": "this post was manually entered in codio's backend"}
]


def valid_post(post):
    if 'title' not in post or 'content' not in post:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = request.get_json()
        if valid_post(new_post):
            new_id = max(post['id'] for post in POSTS) + 1
            new_post['id'] = new_id
            POSTS.append(new_post)
            return jsonify(new_post), 201

        if not valid_post(new_post):
            if 'content' not in new_post and 'title' not in new_post:
                return jsonify({"error": "missing post title and content"}), 400
            elif 'content' in new_post:
                return jsonify({"error": "missing post title"}), 400
            elif 'title' in new_post:
                return jsonify({"error": "missing post content"}), 400

    elif request.method == 'GET':
        sort = request.args.get('sort')
        direction = request.args.get('direction')
        if not sort and not direction:
            return jsonify(POSTS)
        elif sort and direction:
            if sort == 'title' and direction == 'asc':
                return jsonify(sorted(POSTS, key=lambda post: post['title']))
            if sort == 'title' and direction == 'desc':
                return jsonify(sorted(POSTS, key=lambda post: post['title'], reverse=True))
            if sort == 'content' and direction == 'asc':
                return jsonify(sorted(POSTS, key=lambda post: post['content']))
            if sort == 'content' and direction == 'desc':
                return jsonify(sorted(POSTS, key=lambda post: post['content'], reverse=True))
        else:
            return jsonify({"error": "invalid sorting"}), 400


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    updated_post = request.get_json()
    for post in POSTS:
        if post['id'] == post_id:
            post.update(updated_post)
            return jsonify(post)
    return jsonify({"error": "Post not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})
    return jsonify({"error": "Post not found."}), 404


@app.route('/api/posts/search')
def find_post():
    title = request.args.get('title')
    content = request.args.get('content')
    search_output = []
    for post in POSTS:
        if title and title in post['title'] or content and content in post['content']:
            search_output.append(post)
    return jsonify(search_output)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
