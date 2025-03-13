import random
from flask import render_template, request, redirect, url_for, session, flash
from app.database import db
from ..database.models.User import User
from flask_mail import Message
import secrets

from . import login_bp
from ..extensions import mail

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('login_bp.register'))

        new_user = User(
            email=email,
            username=username,
            balance=random.randint(100, 500) 
        )
        new_user.password = password 

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login_bp.login'))

    return render_template('register.html')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id 
            session['email'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('home.dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login_bp.login'))

reset_tokens = {}

@login_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = db.session.query(User).filter_by(email=email).first()

        if user:
            token = secrets.token_urlsafe(32)  # Generate a secure token
            reset_tokens[token] = user.email  # Store token-email pair temporarily

            # Send reset email
            reset_link = url_for('login_bp.reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f"Click the link below to reset your password:\n{reset_link}"
            mail.send(msg)

            flash('If the email exists, a reset link has been sent.', 'info')
            return redirect(url_for('login_bp.login'))

        flash('If the email exists, a reset link has been sent.', 'info')

    return render_template('forgot_password.html')

@login_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = reset_tokens.get(token)

    if not email:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('login_bp.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('login_bp.reset_password', token=token))

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            user.password = password  # Hashing is handled in the model
            db.session.commit()
            del reset_tokens[token]  # Remove token after use

            flash('Password updated successfully! You can now log in.', 'success')
            return redirect(url_for('login_bp.login'))

        flash('User not found.', 'danger')

    return render_template('reset_password.html', token=token)