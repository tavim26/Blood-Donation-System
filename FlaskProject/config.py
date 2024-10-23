import os

class Config:
    # Setează calea completă pentru baza de date
    BASEDIR = os.path.abspath(os.path.dirname(__file__))  # Directorul în care se află config.py
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASEDIR, "database.sqlite")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Adaugă secret_key pentru sesiune
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')