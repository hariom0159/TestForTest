from datetime import datetime, timedelta

# Reg-B protected attributes
PROTECTED_ATTRIBUTES = ["race", "gender", "age", "marital_status", "national_origin"]

def validate_reg_b(loan):
    """Check for Reg-B compliance issues in the loan application."""
    errors = []

    # Check for protected attributes
    for attr in PROTECTED_ATTRIBUTES:
        if getattr(loan, attr, None):
            errors.append(f"Protected attribute '{attr}' used in lending decision.")

    # Check for decision notification within 30 days
    application_date = datetime.strptime(loan.application_date, "%Y-%m-%d")
    decision_date = datetime.strptime(loan.decision_date, "%Y-%m-%d")
    if (decision_date - application_date).days > 30:
        errors.append("Loan decision notification exceeded the 30-day limit.")

    compliant = len(errors) == 0

    return {
        "compliant": compliant,
        "errors": errors
    }

def validate_small_business_reg_b(loan):
    """
    Validate Reg-B compliance for small businesses (< $1M revenue)
    - Must notify of credit decision within 30 days
    """
    errors = []

    application_date = datetime.strptime(loan.application_date, "%Y-%m-%d")
    decision_date = datetime.strptime(loan.decision_date, "%Y-%m-%d")

    if (decision_date - application_date).days > 30:
        errors.append("Loan decision notification exceeded the 30-day limit for small businesses.")

    compliant = len(errors) == 0

    return {
        "compliant": compliant,
        "errors": errors
    }
