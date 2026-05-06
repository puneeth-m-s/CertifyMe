from flask import Blueprint, request, jsonify
from app import db, jwt
from app.models import Admin
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required'}), 400

    if Admin.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    admin = Admin(username=username, email=email)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    return jsonify({'message': 'Admin created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    admin = Admin.query.filter_by(email=email).first()
    if not admin or not admin.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(admin.id))
    refresh_token = create_refresh_token(identity=str(admin.id))

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({'message': 'Email not found'}), 404

    # Generate reset token with expiry (e.g., 1 hour)
    reset_token = create_access_token(identity=str(admin.id), expires_delta=datetime.timedelta(hours=1))

    # In a real app, send email with reset_token
    # For demo, return the token
    return jsonify({'message': 'Reset token generated', 'reset_token': reset_token}), 200

@auth_bp.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    data = request.get_json()
    new_password = data.get('new_password')

    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({'message': 'Admin not found'}), 404

    admin.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200