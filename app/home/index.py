from flask import session, redirect, url_for, flash, render_template
from . import home

@home.route('/')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for('login_bp.login')) 

    return render_template("home.html")