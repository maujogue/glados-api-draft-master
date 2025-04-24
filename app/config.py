import os


class Config(object):
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL")


class ProductionConfig(Config):
    ENV = "production"


class DevelopmentConfig(Config):
    ENV = "development"


class TestingConfig(Config):
    ENV = "test"
    TESTING = True

    # Database
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:root@db_test/glados"
    OPENDATA_DATABASE_URI = "postgresql+psycopg2://postgres:root@db_test/glados"


CONFIG_MAP = {
    "production": ProductionConfig,
    "test": TestingConfig,
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}
