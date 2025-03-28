from flask import Flask

# blueprint imports
from routes.login_bp import login_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(login_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
