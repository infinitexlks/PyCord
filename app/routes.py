from flask import Blueprint, request, jsonify
from app.extensions import db, jwt, socketio
from app.models import User, Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@jwt_required()
@main.route('/messages', methods=['POST'])
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_message = Message(content=data['content'], user_id=user_id)
    db.session.add(new_message)
    db.session.commit()
    socketio.emit('new_message', {'content': data['content'], 'username': User.query.get(user_id).username})
    return jsonify(message="Message sent"), 201

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
