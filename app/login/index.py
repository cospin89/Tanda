from flask import render_template, request, redirect, url_for, session, flash
from app.database import db
from ..database.models.User import User

from . import login_bp

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
