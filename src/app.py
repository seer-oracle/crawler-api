# -*- coding: utf-8 -*-

import sentry_sdk
from pymodm import connect
from sentry_sdk import capture_exception, capture_message
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request, jsonify

from .config import DefaultConfig
from flask_cors import CORS
import atexit
from src.services import price
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timezone
import pytz
from src.schedule.schedules import ScheduleService
import asyncio
from src.extensions import Extensions



# For import *
__all__ = ['create_app']


def create_app(config=None, app_name=None):
    """Create a Flask app."""
    if app_name is None:
        app_name = DefaultConfig.PROJECT
    tz = pytz.timezone('Asia/Ho_Chi_Minh')

    app = Flask(app_name, instance_relative_config=True)

    configure_app(app, config)
    configure_hook(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_template_filters(app)
    configure_logging_level() 
    
    scheduler = BackgroundScheduler()
    executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler.configure(executors=executors, job_defaults=job_defaults)
   
    scheduler.add_job(func=ScheduleService.get_price, 
                        trigger="interval", timezone=tz,
                        seconds=5)
 
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)



def configure_extensions(app):
    connect(DefaultConfig.MONGODB_URI, connect=False)

    # Sentry
    if DefaultConfig.SENTRY_DSN:
        sentry_sdk.init(
            dsn=DefaultConfig.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            server_name=DefaultConfig.PROJECT
        )

        capture_message('{} starts'.format(DefaultConfig.PROJECT))


def configure_blueprints(app):
    """Configure blueprints in views."""
    from src.api import DEFAULT_BLUEPRINTS as blueprints
    for blueprint in blueprints:
        app.register_blueprint(
            blueprint,
            url_prefix=f'/{blueprint.url_prefix}'
        )


def configure_template_filters(app):
    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_logging_level():
    import logging
    logging.getLogger('suds').setLevel(logging.ERROR)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass



