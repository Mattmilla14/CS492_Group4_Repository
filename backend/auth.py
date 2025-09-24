# This file contains authentication helpers
# It checks if users are logged in and what they're allowed to do

from functools import wraps
from flask import request, jsonify, current_app
from models import User
import jwt

def token_required(f):
    """
    This is a decorator that checks if a user is logged in
    We put @token_required above any function that needs authentication
    It's like a security guard that checks your ID before letting you in
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in the Authorization header
        # The frontend sends: Authorization: Bearer <token>
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Extract the token (remove "Bearer " from the beginning)
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid token format. Use: Bearer <token>'
                }), 401
        
        # If no token was provided
        if not token:
            return jsonify({
                'success': False,
                'error': 'Access token is missing! Please log in.'
            }), 401
        
        try:
            # Verify the token and get the user
            current_user = User.verify_token(token)
            if current_user is None:
                return jsonify({
                    'success': False,
                    'error': 'Token is invalid or expired!'
                }), 401
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Token verification failed!'
            }), 401
        
        # If everything is OK, call the original function
        # and pass the current_user as a parameter
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """
    This decorator checks if a user is an admin
    Use @admin_required for functions that only admins can access
    """
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({
                'success': False,
                'error': 'Admin access required!'
            }), 403  # 403 means "Forbidden"
        
        return f(current_user, *args, **kwargs)
    
    return decorated