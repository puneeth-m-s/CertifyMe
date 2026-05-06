from flask import Blueprint, request, jsonify
from app import db
from app.models import Admin
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
import datetime
import re

auth_bp = Blueprint('auth', __name__)

# -----------------------------
# Admin Signup
# -----------------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    print("Signup Data:", data)

    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Validate required fields
    if not full_name or not email or not password or not confirm_password:
        return jsonify({
            'message': 'All fields are required'
        }), 400

    # Email validation
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_regex, email):
        return jsonify({
            'message': 'Invalid email format'
        }), 400

    # Password length validation
    if len(password) < 8:
        return jsonify({
            'message': 'Password must be at least 8 characters'
        }), 400

    # Confirm password validation
    if password != confirm_password:
        return jsonify({
            'message': 'Passwords do not match'
        }), 400

    # Check existing email
    existing_admin = Admin.query.filter_by(email=email).first()

    if existing_admin:
        return jsonify({
            'message': 'Account already exists'
        }), 400

    # Create admin
    admin = Admin(
        username=full_name,
        email=email
    )

    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

    return jsonify({
        'message': 'Admin account created successfully'
    }), 201


# -----------------------------
# Admin Login
# -----------------------------
@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    print("Login Data:", data)

    email = data.get('email')
    password = data.get('password')

    # Validate fields
    if not email or not password:
        return jsonify({
            'message': 'Email and password are required'
        }), 400

    # Find admin
    admin = Admin.query.filter_by(email=email).first()

    # Generic error message
    if not admin or not admin.check_password(password):
        return jsonify({
            'message': 'Invalid email or password'
        }), 401

    # Generate JWT tokens
    access_token = create_access_token(
        identity=str(admin.id)
    )

    refresh_token = create_refresh_token(
        identity=str(admin.id)
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'admin': {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email
        }
    }), 200


# -----------------------------
# Forgot Password
# -----------------------------
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():

    data = request.get_json()

    print("Forgot Password Data:", data)

    email = data.get('email')

    if not email:
        return jsonify({
            'message': 'Email is required'
        }), 400

    admin = Admin.query.filter_by(email=email).first()

    # Always show same response
    if admin:

        reset_token = create_access_token(
            identity=str(admin.id),
            expires_delta=datetime.timedelta(hours=1)
        )

        # Log token internally
        print("Reset Token:", reset_token)

    return jsonify({
        'message': 'If the email exists, a reset link has been generated'
    }), 200


# -----------------------------
# Reset Password
# -----------------------------
@auth_bp.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():

    data = request.get_json()

    print("Reset Password Data:", data)

    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    # Validate fields
    if not new_password or not confirm_password:
        return jsonify({
            'message': 'All fields are required'
        }), 400

    # Password length validation
    if len(new_password) < 8:
        return jsonify({
            'message': 'Password must be at least 8 characters'
        }), 400

    # Password match validation
    if new_password != confirm_password:
        return jsonify({
            'message': 'Passwords do not match'
        }), 400

    admin_id = int(get_jwt_identity())

    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({
            'message': 'Admin not found'
        }), 404

    # Update password
    admin.set_password(new_password)

    db.session.commit()

    return jsonify({
        'message': 'Password reset successfully'
    }), 200