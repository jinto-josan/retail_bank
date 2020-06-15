import os

class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'adasde23324asdk@'
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.sqlite')
