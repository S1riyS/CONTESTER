from config import Config


class TestConfig(Config):
    """Basic application config for tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None
