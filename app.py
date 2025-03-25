from flask import Flask, request, jsonify
from modules.config import Config
from modules.models import db, LoanApplication
from modules.compliance import validate_compliance
from modules.regb import validate_reg_b

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize DB
with app.app_context():
    db.create_all()

@app.route('/apply-loan', methods=['POST'])
def apply_loan():
    data = request.json

    # Create Loan Application
    loan = LoanApplication(
        applicant_name=data.get('name'),
        income=data.get('income'),
        credit_score=data.get('credit_score'),
        kyc_status=data.get('kyc_status'),
        race=data.get('race'),
        gender=data.get('gender'),
        age=data.get('age'),
        marital_status=data.get('marital_status'),
        national_origin=data.get('national_origin'),
        application_date=data.get('application_date'),
        decision_date=data.get('decision_date')
    )

    # Validate general lending compliance
    compliance_result = validate_compliance(loan)

    # Validate Reg-B compliance
    reg_b_result = validate_reg_b(loan)

    if compliance_result['compliant'] and reg_b_result['compliant']:
        db.session.add(loan)
        db.session.commit()
        return jsonify({
            "message": "Loan application submitted successfully!",
            "status": "Approved"
        }), 200
    else:
        return jsonify({
            "message": "Loan application failed compliance check",
            "errors": compliance_result['errors'] + reg_b_result['errors']
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
