from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models import db, JobRole, User

seeker_bp = Blueprint('seeker_bp', __name__)

@seeker_bp.route('/seeker_dashboard', methods=['GET', 'POST'])
def seeker_dashboard():
    user_id = request.args.get('user_id')
    if not user_id:
        pass
    user = User.query.get_or_404(user_id)
    search_area = session.get('search', user.area)
    if request.method == 'POST':
        search_area = request.form.get('search_area')
        job_roles = JobRole.query.filter(JobRole.requirements==search_area).all()
    else:
        job_roles = JobRole.query.filter(JobRole.requirements==user.area).all()
    return render_template('seeker_dashboard.html', username=user.username, job_roles=job_roles, area=user.area,user_id=user.id)

@seeker_bp.route('/view_job_roles/<int:job_role_id>', methods=['GET', 'POST'])
def view_job_roles(job_role_id):
    user_id = session.get('user_id')
    if not user_id:
        pass
    job_role = JobRole.query.get_or_404(job_role_id)
    company_id=job_role.company_id
    user=User.query.get_or_404(company_id)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'accept':
            job_role.status = 'Accepted'
        elif action == 'reject':
            job_role.status = 'Rejected'
        elif action == 'negotiate':
            new_payment = request.form.get('new_payment')
            job_role.payment_amount = new_payment
            job_role.status = 'Negotiated'
        db.session.commit()
        return redirect(url_for('seeker_bp.view_job_roles', job_role_id=job_role_id,user=user))
    return render_template('view_job_roles.html', job_role=job_role,user=user)

@seeker_bp.route('/update_seeker', methods=['GET', 'POST'])
def update_seeker():
    seeker_id = session.get('user_id')
    if not seeker_id:
        return redirect(url_for('auth_bp.login'))
    user = User.query.get_or_404(seeker_id)
    if request.method == 'POST':
        user.area = request.form.get('area')
        db.session.commit()
        return redirect(url_for('seeker_bp.seeker_dashboard'))
    return render_template('update_seeker.html', user=user)
