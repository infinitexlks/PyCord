from flask import Flask
from app.extensions import db, jwt, socketio
from app.routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(main)

    return app
