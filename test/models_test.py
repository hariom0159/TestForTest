from modules.models import LoanApplication

def test_loan_application_model():
    """Test LoanApplication model instance creation"""
    loan = LoanApplication(
        applicant_name="Alice",
        income=50000,
        credit_score=750,
        kyc_status=True
    )

    assert loan.applicant_name == "Alice"
    assert loan.income == 50000
    assert loan.credit_score == 750
    assert loan.kyc_status is True
    assert loan.status == "Pending"
