import os


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/tavim/Desktop/Projects/Blood-Donation-System/FlaskProject/database.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
