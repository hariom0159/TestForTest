import pytest
from app import app, db
from modules.models import LoanApplication

@pytest.fixture
def client():
    # Setup Flask test client
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_apply_loan_success(client):
    """Test a successful loan application"""
    response = client.post('/apply-loan', json={
        "name": "John Doe",
        "income": 30000,
        "credit_score": 700,
        "kyc_status": True
    })
    assert response.status_code == 200
    assert response.json['status'] == "Approved"

def test_apply_loan_failure(client):
    """Test loan application failing compliance checks"""
    response = client.post('/apply-loan', json={
        "name": "Jane Doe",
        "income": 15000,  # Below income threshold
        "credit_score": 600,  # Low credit score
        "kyc_status": False  # KYC not completed
    })
    assert response.status_code == 400
    assert "Loan application failed compliance check" in response.json['message']
    assert "Income below minimum threshold" in response.json['errors']
    assert "Credit score too low" in response.json['errors']
    assert "KYC not completed" in response.json['errors']
