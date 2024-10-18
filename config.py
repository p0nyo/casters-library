from os import environ
from dotenv import load_dotenv

load_dotenv()

# assert environ.get('FLASK_APP') == 'wsgi.py'


class Config:
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    TESTING = environ.get('TESTING')
    REPOSITORY = environ.get('REPOSITORY')
