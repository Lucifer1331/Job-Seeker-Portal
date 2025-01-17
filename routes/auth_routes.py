from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/')
def index():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        if user.role=="company":
            return redirect(url_for('auth_bp.userprofilecompany', user_id=user.id))
        elif user.role=="admin":
            return redirect(url_for('admin_bp.admin_dashboard'))
        else:
            session['user_id']=user.id
            return redirect(url_for("auth_bp.userprofileseeker",user_id=user.id))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_bp.admin_dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company_bp.company_dashboard', user_id=user.id))
            elif user.role == 'seeker':
                return redirect(url_for('seeker_bp.seeker_dashboard', user_id=user.id))
        else:
            return redirect(url_for('auth_bp.logout'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.index'))

@auth_bp.route('/userprofilecompany', methods=['GET', 'POST'])
def userprofilecompany():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if request.method == 'POST':
        category = request.form.get('category')
        budget = request.form.get('budget')
        user.category = category
        user.budget = budget
        db.session.commit()
        session['user_id']=user.id
        return redirect(url_for('company_bp.company_dashboard', user_id=user.id))
    return render_template('userprofilecompany.html', user=user)

@auth_bp.route('/userprofileseeker', methods=['GET', 'POST'])
def userprofileseeker():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if request.method == 'POST':
        area = request.form.get('area')
        user.area = area
        db.session.commit()
        session['user_id']=user.id
        return redirect(url_for('seeker_bp.seeker_dashboard', user_id=user.id))
    return render_template('userprofileseeker.html', user=user)

