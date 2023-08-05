import os

_project_root = os.environ.get("PROJECT_ROOT")
_default_profile_image_folder = os.path.join(
    _project_root, "app", "static", "images", "default_user_images"
)


def get_default_images():
    """
    Get the default images of the user.
    @return: The default images of the user.
    """
    return [
        os.path.join(_default_profile_image_folder, filename)
        for filename in os.listdir(_default_profile_image_folder)
    ]
