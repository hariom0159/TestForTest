from flask import Flask, request, jsonify
from modules.config import Config
from modules.models import db, LoanApplication
from modules.compliance import validate_compliance
from modules.regb import validate_reg_b, validate_small_business_reg_b

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

    # Apply Small Business Compliance Check
    reg_b_result = validate_small_business_reg_b(loan)

    if reg_b_result['compliant']:
        db.session.add(loan)
        db.session.commit()
        return jsonify({
            "message": "Loan application approved for small business",
            "status": "Approved"
        }), 200
    else:
        return jsonify({
            "message": "Loan application failed compliance check",
            "errors": reg_b_result['errors']
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
