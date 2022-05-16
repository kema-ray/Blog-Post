from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import InputRequired

class BlogForm(FlaskForm):

    title = StringField('Blog title',validators=[InputRequired()])
    post = TextAreaField('Post',validators=[InputRequired()])
    author=StringField('Author',validators=[InputRequired()])
    submit = SubmitField('Submit')

class UpdateBlog(FlaskForm):
    title = StringField('Enter title',validators=[InputRequired()])
    blog = TextAreaField('Edit your blog',validators = [InputRequired()])
    submit = SubmitField('Submit') 

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Bio',validators = [InputRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment:',validators=[InputRequired()])
    submit = SubmitField('Submit')