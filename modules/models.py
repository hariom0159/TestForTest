from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    income = db.Column(db.Float, nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    kyc_status = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default="Pending")
