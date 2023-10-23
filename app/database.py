import logging
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.WARNING)


class Database:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance.db = SQLAlchemy()
                logging.info("Database instance created successfully.")
            except Exception as e:
                logging.error(f"Error occurred while creating database instance: {e}")
        return cls._instance

    def init_app(self, app):
        try:
            self.db.init_app(app)
            with app.app_context():
                self.db.create_all()
            logging.info("Database initialized and all tables created successfully.")
        except Exception as e:
            logging.error(f"Error occurred while initializing database or creating tables: {e}")

    def get_db(self):
        return self.db
