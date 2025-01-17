from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from routes.seeker_routes import seeker_bp
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(seeker_bp)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
