from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from routes.auth import auth_bp
    from routes.documents import documents_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(documents_bp, url_prefix="/documents")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        import models  # noqa: F401
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
