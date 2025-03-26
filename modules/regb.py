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

def validate_large_small_business_reg_b(loan):
    """
    Validate Reg-B for small businesses (> $1M revenue)
    - Provide reasons for adverse action if requested within 60 days
    """
    errors = []

    decision_date = datetime.strptime(loan.decision_date, "%Y-%m-%d")
    request_date = datetime.strptime(loan.request_date, "%Y-%m-%d") if loan.request_date else None

    if request_date:
        # Ensure adverse action reason is provided within 60 days
        if (request_date - decision_date).days > 60:
            errors.append("Failure to provide reasons for adverse action within 60 days for large small business.")

    compliant = len(errors) == 0

    return {
        "compliant": compliant,
        "errors": errors
    }
