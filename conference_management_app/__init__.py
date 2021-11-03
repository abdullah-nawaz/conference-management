from contextlib import contextmanager

from flask import Flask
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import flask_config, SQLAlchemyConfig

compress = Compress()
db = SQLAlchemy()
Session = sessionmaker(bind=create_engine(
    SQLAlchemyConfig.SQLALCHEMY_DATABASE_URI, pool_size=SQLAlchemyConfig.SQLALCHEMY_POOL_SIZE,
    max_overflow=SQLAlchemyConfig.SQLALCHEMY_MAX_OVERFLOW, pool_recycle=SQLAlchemyConfig.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=SQLAlchemyConfig.SQLALCHEMY_POOL_TIMEOUT))


@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_app(environment):
    app = Flask(__name__)
    config = flask_config[environment]
    app.config.from_object(config)
    app.logger.setLevel(config.LOGGING_LEVEL_MAPPED)
    compress.init_app(app)
    db.init_app(app)
    db.app = app

    from conference_management_app.web.conferences import \
        conference_management_conference as conference_management_conference_blueprint

    app.register_blueprint(conference_management_conference_blueprint, url_prefix="/v1/conference-management")

    return app
