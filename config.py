import os


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    POSTGREST_DATABASE_URI = os.getenv('DATABASE_URL')
    DB_NAME = os.getenv('DB_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    TEST_DB = os.environ.get('TEST_DB')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # POSTGREST_DATABASE_URI = os.environ.get('TEST_DB')


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

AppConfig = TestingConfig if os.getenv('APP_SETTINGS') == 'testing' else app_config.get(
    os.getenv('FLASK_ENV'), 'development')