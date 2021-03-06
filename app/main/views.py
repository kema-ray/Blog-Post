from click import edit
from flask import redirect, render_template,url_for,request,abort
from . import main
from ..models import Blog,User,Comment
from .forms import BlogForm,UpdateProfile,CommentForm
from flask_login import login_required,current_user
from .. import db,photos
import datetime
from ..request import get_quotes

@main.route('/')
def index():

    title = 'P-Blogs'
    random_quotes=get_quotes()
    post=Blog.query.all()
    
    return render_template('index.html',title=title,quote=random_quotes,post=post)
@main.route('/blog/<int:blog_id>',methods=["GET"])
def blog(blog_id):
    form = CommentForm()
    blogs = Blog.query.get(blog_id)

    return render_template('blogs.html',blog=blogs,form=form)

@main.route('/blog/new',methods=["GET","POST"])
@login_required
def new_Blog():
     form = BlogForm()
     if form.validate_on_submit():
         title=form.title.data
         post=form.post.data
         author=form.author.data
         user_id=current_user

         new_blogs_object=Blog(user_id=current_user._get_current_object().id,author=author,post=post,title=title)
         new_blogs_object.save_blog()
         return redirect(url_for('main.index'))

     title = 'New Blog'
     return render_template('newBlog.html',form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    post = Blog.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,post = post)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/<blog_id>/',methods=['GET','DELETE'])
@login_required
def deleteBlogs(blog_id):
    deleteBlog = Blog.query.filter_by(id=blog_id).first()
    if deleteBlog:
        db.session.delete(deleteBlog)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        pass
    return redirect(url_for('main.index'))

@main.route('/blog/edit/<int:id>',methods=['GET','POST'])
@login_required
def editBlogs(id):
    if not current_user:
        abort (404)
    edit_blog=Blog.query.get(id)
    form = BlogForm()
    if form.validate_on_submit():
        edit_blog.title= form.title.data
        edit_blog.post = form.post.data
        db.session.add(edit_blog)
        db.session.commit()
        return redirect(url_for('main.index',id=edit_blog.id))
    form.title.data=edit_blog.title
    form.post.data=edit_blog.post
    return render_template('newBlog.html',form=form)

@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
@login_required
def comment(blog_id):
  coments = Comment.query.filter_by(blog_id=blog_id).all()
  form = CommentForm()
  if form.validate_on_submit():
    comment = form.comment.data

    new_comment_object = Comment(comment=comment, blog_id=blog_id, user_id = current_user._get_current_object().id)

    new_comment_object.save_comment()
    return redirect(url_for('main.comment', blog_id=blog_id))

  return render_template('comment.html',form=form,coments=coments)



