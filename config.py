import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'content.db')
SECRET_KEY = 'ai_repurposer_2024_secret'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
ALLOWED_AUDIO = {'wav', 'mp3', 'ogg', 'm4a'}
