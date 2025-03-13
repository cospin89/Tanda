from flask import session, redirect, url_for, flash, render_template, request
from . import home
from app.database import db
from app.database.models.User import User
from app.database.models.Tanda import Tanda, TandaMember

@home.route('/')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for('login_bp.login')) 

    user = db.session.get(User, session['user_id'])
    tandas = db.session.query(Tanda).all()
    user_tandas = db.session.query(TandaMember).filter_by(user_id=user.id).all()

    return render_template("home.html", user=user, tandas=tandas, user_tandas=user_tandas)


@home.route('/tanda/create', methods=['POST'])
def create_tanda():
    if 'user_id' not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for('login_bp.login')) 

    name = request.form.get('name')
    price = request.form.get('price')

    if not name or not price:
        flash("All fields are required!", "danger")
        return redirect(url_for('home.dashboard'))

    new_tanda = Tanda(name=name, price_per_user=float(price), created_by=session['user_id'])
    db.session.add(new_tanda)
    db.session.commit()
    flash("Tanda created successfully!", "success")
    return redirect(url_for('home.dashboard'))


@home.route('/tanda/join/<int:tanda_id>')
def join_tanda(tanda_id):
    if 'user_id' not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for('login_bp.login')) 

    user_id = session['user_id']
    existing_member = db.session.query(TandaMember).filter_by(user_id=user_id, tanda_id=tanda_id).first()

    if existing_member:
        flash("You are already a member of this Tanda!", "warning")
        return redirect(url_for('home.dashboard'))

    new_member = TandaMember(user_id=user_id, tanda_id=tanda_id)
    db.session.add(new_member)
    db.session.commit()
    flash("You have joined the Tanda!", "success")
    return redirect(url_for('home.dashboard'))


@home.route('/tanda/pay/<int:tanda_id>')
def pay_tanda(tanda_id):
    if 'user_id' not in session:
        flash("You need to log in first!", "warning")
        return redirect(url_for('login_bp.login')) 

    user = db.session.get(User, session['user_id'])
    tanda = db.session.get(Tanda, tanda_id)
    member = db.session.query(TandaMember).filter_by(user_id=user.id, tanda_id=tanda_id).first()

    if not member:
        flash("You are not part of this Tanda!", "danger")
        return redirect(url_for('home.dashboard'))

    if user.balance < tanda.price_per_user:
        flash("Insufficient balance to pay!", "danger")
        return redirect(url_for('home.dashboard'))

    user.balance -= tanda.price_per_user
    member.has_paid = True
    db.session.commit()
    flash("Payment successful!", "success")
    return redirect(url_for('home.dashboard'))
