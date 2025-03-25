from datetime import datetime, timedelta
from modules.regb import validate_reg_b, validate_small_business_reg_b
from modules.models import LoanApplication

def test_reg_b_compliance_success():
    """Test Reg-B compliance for valid loan application"""
    loan = LoanApplication(
        race=None,
        gender=None,
        age=None,
        marital_status=None,
        national_origin=None,
        application_date="2025-03-01",
        decision_date="2025-03-10"
    )

    result = validate_reg_b(loan)
    assert result['compliant'] is True
    assert len(result['errors']) == 0

def test_reg_b_protected_attributes():
    """Test Reg-B violation due to protected attributes"""
    loan = LoanApplication(
        race="Asian",
        gender="Male",
        age=45,
        marital_status="Married",
        national_origin="India",
        application_date="2025-03-01",
        decision_date="2025-03-10"
    )

    result = validate_reg_b(loan)
    assert result['compliant'] is False
    assert "Protected attribute 'race' used in lending decision." in result['errors']
    assert "Protected attribute 'gender' used in lending decision." in result['errors']

def test_reg_b_30_day_limit():
    """Test Reg-B violation due to late notification"""
    loan = LoanApplication(
        race=None,
        gender=None,
        age=None,
        marital_status=None,
        national_origin=None,
        application_date="2025-03-01",
        decision_date="2025-04-15"  # Exceeds 30-day limit
    )

    result = validate_reg_b(loan)
    assert result['compliant'] is False
    assert "Loan decision notification exceeded the 30-day limit." in result['errors']

def test_small_business_30_day_limit():
    """Test 30-day decision limit for small business"""
    loan = LoanApplication(
        revenue=900000,  # Small business
        application_date="2025-03-01",
        decision_date="2025-03-25"  # Within 30 days
    )

    result = validate_small_business_reg_b(loan)
    assert result['compliant'] is True
    assert len(result['errors']) == 0

def test_small_business_exceeds_30_days():
    """Test failure for exceeding 30-day limit"""
    loan = LoanApplication(
        revenue=900000,  
        application_date="2025-03-01",
        decision_date="2025-04-15"  # Exceeds 30 days
    )

    result = validate_small_business_reg_b(loan)
    assert result['compliant'] is False
    assert "Loan decision notification exceeded the 30-day limit for small businesses." in result['errors']