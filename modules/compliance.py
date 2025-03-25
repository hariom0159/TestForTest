def validate_compliance(loan):
    errors = []

    # Income threshold check
    if loan.income < 20000:
        errors.append("Income below minimum threshold")

    # Credit score check
    if loan.credit_score < 650:
        errors.append("Credit score too low")

    # KYC status check
    if not loan.kyc_status:
        errors.append("KYC not completed")

    compliant = len(errors) == 0

    return {
        "compliant": compliant,
        "errors": errors
    }
