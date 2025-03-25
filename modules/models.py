from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    income = db.Column(db.Float, nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    kyc_status = db.Column(db.Boolean, default=False)
    
    # Reg-B Fields
    race = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)
    national_origin = db.Column(db.String(50), nullable=True)

    application_date = db.Column(db.String(10), nullable=False)
    decision_date = db.Column(db.String(10), nullable=True)

    status = db.Column(db.String(20), default="Pending")
