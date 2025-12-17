import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'bookmarks.db')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True