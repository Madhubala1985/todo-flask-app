from flask import Flask
from flask_login import LoginManager
from app.models import db, User
from app.routes.auth import auth_bp
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'top_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    return app
