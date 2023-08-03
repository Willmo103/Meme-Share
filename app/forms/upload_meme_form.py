# filename: test_memes.py
# filepath: app\scripts\test_memes.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, BooleanField
from wtforms.validators import Length


class UploadMemeForm(FlaskForm):
    """Form for uploading a meme.
    @field image: The image file of the meme.
    @field url: The URL of the meme.
    @field private: Whether the meme is private.
    @field submit: The submit button."""

    image = FileField("Image")
    url = StringField("URL", validators=[Length(min=0, max=1000)])
    private = BooleanField("Private", default=False)
    submit = SubmitField("Upload Meme")

    def validate(self):
        if not super(UploadMemeForm, self).validate():
            return False
        if not self.image.data and not self.url.data:
            msg = "Please provide a URL or upload a file."
            self.image.errors.append(msg)
            self.url.errors.append(msg)
            return False
        return True
