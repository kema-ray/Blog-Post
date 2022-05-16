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
    author=db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    comment = db.relationship('Comment',backref = 'blog',lazy = "dynamic")

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_blogs(cls,user):
        user_blogs = Blog.query.filter_by(user = user).all()
        return user_blogs

    @classmethod
    def viewblogs(cls):
        blogs = Blog.query.all()
        return blogs

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    

    def __repr__(self):
        return f'Blog {self.title}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'),nullable = False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def view_comments(cls,blog_id):
        comments = Comment.query.filter_by(blog_id = blog_id).all()
        return comments


    def __repr__(self):
        return f'comment:{self.comment}' 












