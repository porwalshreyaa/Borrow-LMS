from flask import Flask
from .config import Config
from .extensions import db
from .routes import register_routes
from werkzeug.exceptions import HTTPException


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from app.models import user, book, section
        db.create_all()

    register_routes(app)


    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not Found", "message": "Invalid endpoint"}, 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return {"error": e.name, "message": e.description}, e.code
        return {"error": "Internal Server Error", "message": str(e)}, 500

    return app


# (bad pattern)
# from flask import Flask

# @app.errorhandler(Exception)   # ❌ app doesn’t exist yet
# def handle_error(e):
#     return {"error": "Server Error"}, 500
