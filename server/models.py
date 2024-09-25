from datetime import datetime, timedelta
from server import db, login_manager
from flask_login import UserMixin
from flask_jwt_extended import create_access_token, decode_token

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_in=600):
        reset_token = create_access_token(identity={'user_id': self.id},expires_delta=timedelta(seconds=expires_in))
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        try:
            decoded_token = decode_token(token)
            identity = decoded_token.get('sub')
            user_id = identity.get('user_id')
            expiration_time = datetime.fromtimestamp(decoded_token['exp'])
            found_user = User.query.get(user_id)
            return expiration_time > datetime.utcnow(), found_user
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return False, None


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
