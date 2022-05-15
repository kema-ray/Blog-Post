from flask import redirect, render_template,url_for,request,abort
from . import main
from ..models import Pitch,User,Comment,Upvote,Downvote
from .forms import PitchForm,UpdateProfile,CommentForm
from flask_login import login_required,current_user
from .. import db,photos
import datetime

@main.route('/')
def index():

    title = 'Awesome Pitches'

    # marketing_pitches = Pitch.get_pitches('')
    business_pitches = Pitch.get_pitches('business')
    entertainment_pitches = Pitch.get_pitches('entertainment')
    puns_pitches = Pitch.get_pitches('puns')
    
    return render_template('index.html',title = title,business=business_pitches,entertainment=entertainment_pitches,
    puns=puns_pitches)

@main.route('/pitches/business_pitches')
def business_pitches():

    pitches = Pitch.get_pitches('business')

    return render_template("business_pitches.html", pitches = pitches)

@main.route('/pitches/entertainment_pitches')
def entertainment_pitches():

    pitches = Pitch.get_pitches('entertainment')

    return render_template("entertainment_pitches.html", pitches = pitches)

@main.route('/pitches/puns_pitches')
def puns_pitches():

    pitches = Pitch.get_pitches('puns')

    return render_template("puns_pitches.html", pitches = pitches)

@main.route('/pitch/new',methods=["GET","POST"])
@login_required
def new_pitch():
     pitch_form = PitchForm()
     if pitch_form.validate_on_submit():
         title=pitch_form.title.data
         pitch=pitch_form.text.data
         category=pitch_form.category.data

         new_pitch=Pitch(pitch_title=title,pitch_content=pitch,user=current_user,category=category)
         new_pitch.save_pitch()
         return redirect(url_for('.index'))

     title = 'New Pitch'
     return render_template('new_pitch.html',pitch_form=pitch_form,title=title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    posts = Pitch.query.filter_by(user_id = user_id).all()
    pitches_count = Pitch.count_pitches(uname)
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,pitches = pitches_count,posts = posts)

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

@main.route('/comment/<int:pitch_id>',methods=['GET','POST'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    if form.validate_on_submit():
        comment=form.comment.data
        pitch_id=pitch_id
        user_id=current_user._get_current_object().id
        new_comment=Comment(comment=comment,user_id=user_id,pitch_id=pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment',pitch_id=pitch_id))
    return render_template('comment.html',form=form,pitch=pitch,all_comments=all_comments)

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.save_upvote()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    pitch = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, pitch_id=id)
    new_downvote.save_downvote()
    return redirect(url_for('main.index',id = id))


    

