# from app import app
from app.models import Meme
import os

def generate_test_memes():
    memes_dir = os.path.join( os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'test_memes' )
    for meme in os.listdir(memes_dir):
        if meme.endswith('.jpg'):
            meme_path = os.path.join(memes_dir, meme)
            print(meme_path)
            check_meme = Meme.query.filter_by(filename=meme).first()
            print(check_meme)
            # Meme.create(meme_path)

generate_test_memes()
