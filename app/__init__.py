from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.uploader


cloudinary.config(
  cloud_name = "dbxtbus46",
  api_key = "994774263527943",
  api_secret = "HLpoMPuSSuFMTLFeEP805AriVsk",
  secure = True
)


db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/huutinhdoor"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    app.secret_key = "supersecret"
    db.init_app(app)  
    

    from app.main_routes import main
    from app.admin_routes import admin
    app.register_blueprint(admin)
    app.register_blueprint(main)

    return app
