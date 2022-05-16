from datetime import datetime
from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Quote:
    def __init__(self,quote,author):
        self.quote=quote
        self.author=author

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email =  db.Column(db.String(255),unique=True,index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blogs = db.relationship('Blog',backref='user',lazy='dynamic')
    password_secure = db.Column(db.String(255))
    # date_joined = db.Column(db.DateTime,default=datetime.utcnow)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255),nullable=False)
    post = db.Column(db.Text(), nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    

    def __repr__(self):
        return f'Blog {self.title}'












