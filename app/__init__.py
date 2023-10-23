from flask import Flask
from .routes.game import game_blueprint
from app.database import Database
import logging
logging.basicConfig(level=logging.INFO)


def create_app(config_name='config.config.Config'):
    """
        Create and configure a new app instance.

        :param config_name: The configuration name to set up the app instance, defaults to 'config.config.Config'.
        :return: A new, configured instance of the app.
    """
    app = Flask(__name__)
    logging.info('Creating app instance')

    configure_app(app, config_name)
    configure_database(app)
    register_blueprints(app)

    logging.info('App instance created and configured')
    return app

def configure_app(app, config_name):
    """
        Configure the app with the given configuration.

        :param app: App to configure.
        :param config_name: The configuration name to use.
    """
    app.config.from_object(config_name)
    logging.info(f'App configured with {config_name}')


def configure_database(app):
    """
        Configure the database for the Flask app.

        :param app:  app to attach the database to.
    """
    db = Database()
    db.init_app(app)
    logging.info('Database configured')


def register_blueprints(app):
    """
       Register blueprints to the Flask app.

       :param app: The app to register blueprints to.
    """
    app.register_blueprint(game_blueprint)
    logging.info('Blueprints registered')
