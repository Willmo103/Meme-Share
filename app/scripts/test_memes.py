# from app import app
from app.models import Meme
import os

def generate_test_memes():
    memes_dir = os.path.join( os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'test_memes' )
    for meme in os.listdir(memes_dir):
        if meme.endswith('.jpg'):
            meme_path = os.path.join(memes_dir, meme)
            check_meme = Meme.query.filter_by(filename=meme).first()
            if not check_meme:
                print('creating meme')
                meme = Meme.from_upload(meme, 1, False)
                meme.save()
            # Meme.create(meme_path)

generate_test_memes()
