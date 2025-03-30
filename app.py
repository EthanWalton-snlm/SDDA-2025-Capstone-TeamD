from flask import Flask
from sqlalchemy.sql import text

from config import Config
from extensions import db
from routes.admin_bp import admin_bp
from routes.dashboard_bp import dashboard_bp
from routes.home_bp import home_bp

# blueprint imports
from routes.login_bp import login_bp
from routes.signup_bp import signup_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        try:
            result = db.session.execute(text("SELECT 1")).fetchall()
            # movies_objs = Movie.query.all()
            # movies = [movie.to_dict() for movie in movies_objs]
            print("Connection successful:", result)
        except Exception as e:
            print("Error connecting to the database:", e)

    app.register_blueprint(login_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
