from flask import Flask
from models import db
from routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configuration from config.py

    db.init_app(app)  # Initialize SQLAlchemy with the app
    app.register_blueprint(bp)  # Register the blueprint for routes

    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)