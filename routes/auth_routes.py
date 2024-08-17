from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from services.user_service import User
import os

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('recipe_routes.list_recipes'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('auth_routes.login'))
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.get_by_username(username):
            flash('Username already exists.')
            return redirect(url_for('auth_routes.register'))
        user = User.create_user(username, password)
        login_user(user)
        flash('Account created successfully.')
        return redirect(url_for('recipe_routes.list_recipes'))
    return render_template('register.html')

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth_routes.login'))

# Test route for automatic login
@auth_routes.route('/test-login')
def test_login():
    if os.getenv('FLASK_ENV') == 'development':
        user = User.get_by_username('testuser')
        if not user:
            user = User.create_user('testuser', 'testpassword')
        login_user(user)
        flash('Test user logged in successfully.')
        return redirect(url_for('recipe_routes.list_recipes'))
    else:
        return "Test login route is only available in development mode.", 403
