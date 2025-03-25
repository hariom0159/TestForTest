from modules.compliance import validate_compliance
from modules.models import LoanApplication

def test_compliance_success():
    """Test compliance validation for a valid loan"""
    loan = LoanApplication(
        income=60000,
        credit_score=720,
        kyc_status=True
    )

    result = validate_compliance(loan)
    assert result['compliant'] is True
    assert result['errors'] == []

def test_compliance_low_income():
    """Test compliance validation for low income"""
    loan = LoanApplication(
        income=15000,  # Below threshold
        credit_score=720,
        kyc_status=True
    )

    result = validate_compliance(loan)
    assert result['compliant'] is False
    assert "Income below minimum threshold" in result['errors']

def test_compliance_low_credit_score():
    """Test compliance validation for low credit score"""
    loan = LoanApplication(
        income=50000,
        credit_score=600,  # Below threshold
        kyc_status=True
    )

    result = validate_compliance(loan)
    assert result['compliant'] is False
    assert "Credit score too low" in result['errors']

def test_compliance_missing_kyc():
    """Test compliance validation with missing KYC"""
    loan = LoanApplication(
        income=70000,
        credit_score=750,
        kyc_status=False  # KYC not completed
    )

    result = validate_compliance(loan)
    assert result['compliant'] is False
    assert "KYC not completed" in result['errors']
