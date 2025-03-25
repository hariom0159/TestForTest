from modules.config import Config

def test_config():
    """Test configuration values"""
    assert Config.SQLALCHEMY_DATABASE_URI == 'sqlite:///banking.db'
    assert Config.SQLALCHEMY_TRACK_MODIFICATIONS is False
