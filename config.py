import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ETHEREUM_NODE_URL = os.environ.get('ETHEREUM_NODE_URL', 'https://mainnet.infura.io/v3/YOUR-PROJECT-ID')
    
    # Bank API configurations
    EXAMPLE_BANK_API_KEY = os.environ.get('EXAMPLE_BANK_API_KEY', 'your_example_bank_api_key')
    EXAMPLE_BANK_BASE_URL = os.environ.get('EXAMPLE_BANK_BASE_URL', 'https://api.examplebank.com')
    ANOTHER_BANK_API_KEY = os.environ.get('ANOTHER_BANK_API_KEY', 'your_another_bank_api_key')
    ANOTHER_BANK_BASE_URL = os.environ.get('ANOTHER_BANK_BASE_URL', 'https://api.anotherbank.com')
    
    # ACH system configurations
    EXAMPLE_ACH_API_KEY = os.environ.get('EXAMPLE_ACH_API_KEY', 'your_example_ach_api_key')
    EXAMPLE_ACH_BASE_URL = os.environ.get('EXAMPLE_ACH_BASE_URL', 'https://api.exampleach.com')
    ANOTHER_ACH_API_KEY = os.environ.get('ANOTHER_ACH_API_KEY', 'your_another_ach_api_key')
    ANOTHER_ACH_BASE_URL = os.environ.get('ANOTHER_ACH_BASE_URL', 'https://api.anotherach.com')
