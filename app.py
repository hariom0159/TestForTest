from flask import Flask, request, jsonify
from modules.config import Config
from modules.models import db, LoanApplication
from modules.compliance import validate_compliance

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize DB
with app.app_context():
    db.create_all()

@app.route('/apply-loan', methods=['POST'])
def apply_loan():
    data = request.json
    applicant_name = data.get('name')
    income = data.get('income')
    credit_score = data.get('credit_score')
    kyc_status = data.get('kyc_status')

    # Create Loan Application
    loan = LoanApplication(
        applicant_name=applicant_name,
        income=income,
        credit_score=credit_score,
        kyc_status=kyc_status
    )

    # Validate compliance
    compliance_result = validate_compliance(loan)
    
    if compliance_result['compliant']:
        db.session.add(loan)
        db.session.commit()
        return jsonify({
            "message": "Loan application submitted successfully!",
            "status": "Approved"
        }), 200
    else:
        return jsonify({
            "message": "Loan application failed compliance check",
            "errors": compliance_result['errors']
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
