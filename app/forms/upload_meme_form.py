from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, BooleanField
from wtforms.validators import Length, ValidationError


def url_or_file(form, field):
    if not field.data and not form.url.data:
        raise ValidationError("Please provide a URL or upload a file.")


class UploadMemeForm(FlaskForm):
    file = FileField("Image", validators=[url_or_file])
    url = StringField("URL", validators=[Length(min=0, max=1000)])
    private = BooleanField("Private", default=False)
    submit = SubmitField("Upload Meme")
