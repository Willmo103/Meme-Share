from flask import Blueprint
from flask_wtf import FlaskForm
from app.forms import UploadMemeForm

#     FileUploadForm,
#     BookmarkForm,
#     EditFileForm,
# )

endpoint = Blueprint("routes", __name__)

# Inject forms into all templates
@endpoint.context_processor
def inject_forms() -> dict:
    upload_meme_form: FlaskForm = UploadMemeForm()
    return dict(
        upload_form=upload_meme_form,
    )


#     upload_form: FlaskForm = FileUploadForm()
#     bookmark_form: FlaskForm = BookmarkForm()
#     edit_file_form: FlaskForm = EditFileForm()
#     return dict(
#         upload_form=upload_form,
#         bookmark_form=bookmark_form,
#         edit_file_form=edit_file_form,
#     )

from .index import index_page as index_page
from .auth import login as login, logout as logout, register as register
from .meme import upload_meme as upload_meme
from .api_test_routes import fix_memes as fix_memes
from .save import (
    toggle_save_meme as toggle_save_meme,
    toggle_like_meme as toggle_like_meme,
)
from .user import (
    user as user,
    choose_profile_image as choose_profile_image,
    user_id as user_id,
    edit_user as edit_user,
    delete_user as delete_user,
)
