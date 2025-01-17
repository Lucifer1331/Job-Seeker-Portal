from flask import Blueprint, render_template,request
from models import User, Campaign,JobRole
admin_bp = Blueprint('admin_bp', __name__)
@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    admin_id = request.args.get('user_id')
    active_users = User.query.count()
    total_campaigns = Campaign.query.count()
    public_campaigns = Campaign.query.filter_by(visibility='public').count()
    private_campaigns = Campaign.query.filter_by(visibility='private').count()
    campaigns = Campaign.query.filter_by(visibility='public').all()
    return render_template('admin_dashboard.html', active_users=active_users, total_campaigns=total_campaigns, public_campaigns=public_campaigns, private_campaigns=private_campaigns, campaigns=campaigns)
