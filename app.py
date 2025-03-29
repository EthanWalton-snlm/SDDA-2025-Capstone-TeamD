from flask import Flask

from config import Config
from extensions import db
from routes.dashboard_bp import dashboard_bp
from routes.home_bp import home_bp

# blueprint imports
from routes.login_bp import login_bp
from routes.signup_bp import signup_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(login_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
