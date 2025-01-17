from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    budget=db.Column(db.Integer,nullable=True)
    area=db.Column(db.String(50),nullable=True)
    category=db.Column(db.String(50),nullable=True)
    campaigns = db.relationship('Campaign', backref='company', lazy=True)
    job_roles = db.relationship('JobRole', backref='seeker', lazy=True)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    budget = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visibility = db.Column(db.String(50), nullable=False, default='public')
    job_roles = db.relationship('JobRole', backref='campaign', lazy=True)

class JobRole(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
