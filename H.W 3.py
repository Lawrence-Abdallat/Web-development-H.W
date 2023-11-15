from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='posts')
    status = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    following_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())




@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'role': user.role, 'created_at': user.created_at} for user in users]
    return jsonify(user_list)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.username = data['username']
    user.role = data['role']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})



@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    new_post = Post(title=data['title'], body=data['body'], user_id=data['user_id'], status=data['status'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'})


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    post_list = [{'id': post.id, 'title': post.title, 'body': post.body, 'user_id': post.user_id, 'status': post.status, 'created_at': post.created_at} for post in posts]
    return jsonify(post_list)


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    post.title = data['title']
    post.body = data['body']
    post.user_id = data['user_id']
    post.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})


@app.route('/follows', methods=['POST'])
def create_follow():
    data = request.json
    new_follow = Follow(following_user_id=data['following_user_id'], followed_user_id=data['followed_user_id'])
    db.session.add(new_follow)
    db.session.commit()
    return jsonify({'message': 'Follow relationship created successfully'})


@app.route('/follows', methods=['GET'])
def get_follows():
    follows = Follow.query.all()
    follow_list = [{'id': follow.id, 'following_user_id': follow.following_user_id, 'followed_user_id': follow.followed_user_id, 'created_at': follow.created_at} for follow in follows]
    return jsonify(follow_list)

@app.route('/follows/<int:follow_id>', methods=['PUT'])
def update_follow(follow_id):
    data = request.json
    follow = Follow.query.get(follow_id)
    if not follow:
        return jsonify({'message': 'Follow relationship not found'}), 404
    follow.following_user_id = data['following_user_id']
    follow.followed_user_id = data['followed_user_id']
    db.session.commit()
    return jsonify({'message': 'Follow relationship updated successfully'})


@app.route('/follows/<int:follow_id>', methods=['DELETE'])
def delete_follow(follow_id):
    follow = Follow.query.get(follow_id)
    if not follow:
        return jsonify({'message': 'Follow relationship not found'}), 404
    db.session.delete(follow)
    db.session.commit()
    return jsonify({'message': 'Follow relationship deleted successfully'})



