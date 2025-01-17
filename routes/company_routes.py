from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Campaign,User,JobRole

company_bp = Blueprint('company_bp', __name__)

@company_bp.route('/company_dashboard')
def company_dashboard():
    company_id = request.args.get('user_id')
    campaigns = Campaign.query.filter_by(company_id=company_id).all()
    campaigns2=Campaign.query.filter(Campaign.visibility=='public').all()
    user = User.query.get(company_id)
    return render_template('company_dashboard.html', campaigns=campaigns, campaigns2=campaigns2, company_name=user.username, category=user.category, budget=user.budget)

@company_bp.route('/create_campaign', methods=['GET', 'POST'])
def create_campaign():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        budget = request.form['budget']
        visibility = request.form['visibility']
        campaign = Campaign(name=name, description=description, budget=budget, visibility=visibility, company_id=session['user_id'])
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('company_bp.company_dashboard',user_id=campaign.company_id))
    return render_template('create_campaign.html')

@company_bp.route('/view_your_campaigns')
def view_your_campaigns():
    campaigns = Campaign.query.filter_by(company_id=session['user_id']).all()
    return render_template('view_your_campaigns.html', campaigns=campaigns)

@company_bp.route('/view_all_campaigns')
def view_all_campaigns():
    campaigns = Campaign.query.all()
    return render_template('view_all_campaigns.html', campaigns=campaigns)

@company_bp.route('/update_campaign/<int:campaign_id>', methods=['GET', 'POST'])
def update_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if request.method == 'POST':
        x=campaign.budget
        campaign.name = request.form['name']
        campaign.description = request.form['description']
        campaign.budget = request.form['budget']
        campaign.visibility = request.form['visibility']
        company_id = campaign.company_id
        if session.get('user_id')!=company_id:
            user=User.query.get_or_404(session.get('user_id'))
            if user.role=='company':
                return redirect(url_for('company_bp.company_dashboard',user_id=user.id))
        user = User.query.get(company_id)
        user.budget -= int(campaign.budget)-x
        db.session.commit()
        return redirect(url_for('company_bp.company_dashboard', user_id=company_id))
    return render_template('update_campaign.html', campaign=campaign)

@company_bp.route('/campaign_details/<int:campaign_id>')
def campaign_details(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    job_roles = campaign.job_roles  
    return render_template('campaign_details.html', campaign=campaign, job_roles=job_roles,user_id=Campaign.query.get_or_404(campaign_id).company_id)

@company_bp.route('/campaign_details1/<int:campaign_id>')
def campaign_details1(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    job_roles = campaign.job_roles  
    return render_template('campaign_details1.html', campaign=campaign, job_roles=job_roles,user_id=Campaign.query.get_or_404(campaign_id).company_id)

@company_bp.route('/update_company', methods=['GET', 'POST'])
def update_company():
    company_id = session.get('user_id')
    user = User.query.get_or_404(company_id)
    if request.method == 'POST':
        user.category = request.form['category']
        user.budget = request.form['budget']    
        db.session.commit()
        return redirect(url_for('company_bp.company_dashboard', user_id=company_id))
    return render_template('update_company.html', user=user)

@company_bp.route('/create_job_role/<int:campaign_id>', methods=['GET', 'POST'])
def create_job_role(campaign_id):
    company_id = session.get('user_id')
    campaign = Campaign.query.get_or_404(campaign_id)
    if request.method == 'POST':
        details = request.form['details']
        payment = request.form['payment']
        if campaign.company_id != company_id:
            user=User.query.get_or_404(company_id)
            if user.role=='company':
                return redirect(url_for('company_bp.company_dashboard',user_id=company_id))
        else:
            job_role = JobRole(requirements=details, payment_amount=payment, campaign_id=campaign_id, company_id=company_id)
            db.session.add(job_role)
            db.session.commit()
            return redirect(url_for('company_bp.company_dashboard',user_id=company_id))
    return render_template('create_job_role.html', campaign=campaign)

@company_bp.route('/delete_campaign/<int:campaign_id>', methods=['POST'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.company_id != session.get('user_id'):
        return redirect(url_for('company_bp.company_dashboard'))
    JobRole.query.filter_by(campaign_id=campaign_id).delete()
    db.session.delete(campaign)
    db.session.commit()
    return redirect(url_for('company_bp.company_dashboard',user_id=campaign.company_id))

@company_bp.route('/delete_job_role/<int:job_role_id>', methods=['POST'])
def delete_job_role(job_role_id):
    job_role = JobRole.query.get_or_404(job_role_id)
    if job_role.campaign.company_id != session.get('user_id'):
        return redirect(url_for('company_bp.company_dashboard'))
    db.session.delete(job_role)
    db.session.commit()
    return redirect(url_for('company_bp.company_dashboard',user_id=session.get('user_id')))

