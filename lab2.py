from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


# API Resources
class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([{'id': u.id, 'name': u.name} for u in users])

    def post(self):
        data = request.get_json()
        new_user = User(name=data['name'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created'})


class PostResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        posts = Post.query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify([{'id': p.id, 'title': p.title, 'user_id': p.user_id} for p in posts.items])

    def post(self):
        data = request.get_json()
        new_post = Post(title=data['title'], user_id=data['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created'})


class CommentResource(Resource):
    def get(self):
        post_id = request.args.get('post_id', type=int)
        if post_id:
            comments = Comment.query.filter_by(post_id=post_id).all()
        else:
            comments = Comment.query.all()
        return jsonify([{'id': c.id, 'text': c.text, 'post_id': c.post_id} for c in comments])

    def post(self):
        data = request.get_json()
        new_comment = Comment(text=data['text'], post_id=data['post_id'])
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'Comment created'})


# API Routes
api.add_resource(UserResource, '/users')
api.add_resource(PostResource, '/posts')
api.add_resource(CommentResource, '/comments')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
