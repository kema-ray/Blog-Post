import os

# from instance.config import SECRET_KEY
# from distutils.command.config import confSQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@localhost/watchlist'
class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:hotspurs@localhost/bloggers'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")



class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
# .replace("postgres://", "postgresql://",1)
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://qfhuenqqyekkwo:b8b75d4b9e20ebd75946e7ba184d94efa546259530530a4ee33a97169448eff5@ec2-3-229-11-55.compute-1.amazonaws.com:5432/d9sbg9immb45fr'
# DEBUG = True
# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:hotspurs@localhost/pitches_test'


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:hotspurs@localhost/bloggers'
    DEBUG = True

config_options={
    'development':DevConfig,
    'production':ProdConfig
    # 'test':TestConfig
}