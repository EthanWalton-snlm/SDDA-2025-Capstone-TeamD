from flask import Flask
from flask_login import LoginManager
from sqlalchemy.sql import text

from config import Config
from extensions import db
from models.users import User
from routes.account_details_bp import account_details_bp
from routes.admin_bp import admin_bp
from routes.auth_bp import auth_bp
from routes.claims_bp import claims_bp
from routes.dashboard_bp import dashboard_bp
from routes.faq_bp import faq_bp
from routes.home_bp import home_bp
from routes.partners_bp import partners_bp
from routes.policies_bp import policies_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login_page"  # type: ignore

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)  # maintains tokens for specific users

    with app.app_context():
        try:
            result = db.session.execute(text("SELECT 1")).fetchall()
            # movies_objs = Movie.query.all()
            # movies = [movie.to_dict() for movie in movies_objs]
            print("Connection successful:", result)
        except Exception as e:
            print("Error connecting to the database:", e)

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(claims_bp, url_prefix="/claims")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(account_details_bp, url_prefix="/account")
    app.register_blueprint(policies_bp)
    app.register_blueprint(partners_bp)
    app.register_blueprint(faq_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
