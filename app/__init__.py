from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Import config
    from config import Config
    app.config.from_object(Config)
    db.init_app(app)

    cloudinary.config(**app.config['CLOUDINARY'])

    from app.main_routes import main
    from app.admin_routes import admin
    app.register_blueprint(admin)
    app.register_blueprint(main)

    return app
