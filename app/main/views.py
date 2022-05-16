from email.quoprimime import quote
from random import random
from flask import redirect, render_template,url_for,request,abort
from . import main
from ..models import Blog,User,Comment,Upvote,Downvote
from .forms import BlogForm,UpdateProfile,CommentForm
from flask_login import login_required,current_user
from .. import db,photos
import datetime
from ..request import get_quotes

@main.route('/')
def index():

    title = 'P-Blogs'
    random_quotes=get_quotes()
    
    return render_template('index.html',title=title,quote=random_quotes)

@main.route('/Blog/new',methods=["GET","POST"])
@login_required
def new_Blog():
     Blog_form = BlogForm()
     if Blog_form.validate_on_submit():
         title=Blog_form.title.data
         post=Blog_form.post.data
         user_id=current_user

         new_Blog=Blog(user_id=current_user,post=post)
         new_Blog.save_Blog()
         return redirect(url_for('.index'))

     title = 'New Blog'
     return render_template('new_Blog.html',Blog_form=Blog_form,title=title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    posts = Blog.query.filter_by(user_id = user_id).all()
    # blogs_count = Blog.count_blogs(uname)
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts = posts)

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

@main.route('/comment/<int:Blog_id>',methods=['GET','POST'])
@login_required
def comment(Blog_id):
    form = CommentForm()
    Blog = Blog.query.get(Blog_id)
    all_comments = Comment.query.filter_by(Blog_id=Blog_id).all()
    if form.validate_on_submit():
        comment=form.comment.data
        Blog_id=Blog_id
        user_id=current_user._get_current_object().id
        new_comment=Comment(comment=comment,user_id=user_id,Blog_id=Blog_id)
        new_comment.save_comment()
        return redirect(url_for('.comment',Blog_id=Blog_id))
    return render_template('comment.html',form=form,Blog=Blog,all_comments=all_comments)

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_blogs = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for Blog in get_blogs:
        to_str = f'{Blog}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, Blog_id=id)
    new_vote.save_upvote()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    Blog = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in Blog:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, Blog_id=id)
    new_downvote.save_downvote()
    return redirect(url_for('main.index',id = id))


    

