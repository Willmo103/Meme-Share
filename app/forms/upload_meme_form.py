from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

def url_or_file(form, field):
    if not field.data and not form.url.data:
        raise ValidationError('Please provide a URL or upload a file.')

class UploadMemeForm(FlaskForm):
    description = TextAreaField('Description', validators=[Length(min=2, max=1000)])
    image = FileField('Image', validators=[url_or_file])
    url = StringField('URL', validators=[Length(min=0, max=1000)])
    private = BooleanField('Private', default=False)
    submit = SubmitField('Upload Meme')
