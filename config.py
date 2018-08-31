import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    POSTGRES_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    POSTGRES_DATABASE_URI = "postgresql://postgres:sudo!localhost:5432/clvx"


class StagingConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}

