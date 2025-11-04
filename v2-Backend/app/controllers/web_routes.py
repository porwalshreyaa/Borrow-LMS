# app/controllers/web_routes.py

from flask import Blueprint, render_template

# Define the Blueprint
web_bp = Blueprint('web', __name__)

# Example route
@web_bp.route('/')
def home():
    return "<h1>Welcome to Borrow LMS Backend</h1>"

# You can also add more routes:
@web_bp.route('/about')
def about():
    return "<p>This is the Flask backend for Borrow LMS</p>"
