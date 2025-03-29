import requests
from abc import ABC, abstractmethod
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankAPI(ABC):
    @abstractmethod
    def send_transaction(self, transaction_data):
        pass

    @abstractmethod
    def get_transaction_status(self, transaction_id):
        pass

class ACHSystem(ABC):
    @abstractmethod
    def process_ach_transaction(self, ach_data):
        pass

    @abstractmethod
    def get_ach_status(self, ach_id):
        pass

class MockBankAPI(BankAPI):
    def send_transaction(self, transaction_data):
        logger.info(f"Mock bank API: Sending transaction {transaction_data}")
        return {"status": "success", "transaction_id": "mock-123"}

    def get_transaction_status(self, transaction_id):
        logger.info(f"Mock bank API: Getting status for transaction {transaction_id}")
        return {"status": "completed"}

class MockACHSystem(ACHSystem):
    def process_ach_transaction(self, ach_data):
        logger.info(f"Mock ACH system: Processing transaction {ach_data}")
        return {"status": "success", "ach_id": "mock-ach-123"}

    def get_ach_status(self, ach_id):
        logger.info(f"Mock ACH system: Getting status for ACH {ach_id}")
        return {"status": "completed"}

class ExampleBankAPI(BankAPI):
    def __init__(self):
        self.api_key = Config.EXAMPLE_BANK_API_KEY
        self.base_url = Config.EXAMPLE_BANK_BASE_URL

    def send_transaction(self, transaction_data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.post(f"{self.base_url}/transactions", json=transaction_data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending transaction to Example Bank: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_transaction_status(self, transaction_id):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(f"{self.base_url}/transactions/{transaction_id}", headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting transaction status from Example Bank: {str(e)}")
            return {"status": "error", "message": str(e)}

class AnotherBankAPI(BankAPI):
    def __init__(self):
        self.api_key = Config.ANOTHER_BANK_API_KEY
        self.base_url = Config.ANOTHER_BANK_BASE_URL

    def send_transaction(self, transaction_data):
        headers = {"X-API-Key": self.api_key}
        try:
            response = requests.post(f"{self.base_url}/api/v1/transactions", json=transaction_data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending transaction to Another Bank: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_transaction_status(self, transaction_id):
        headers = {"X-API-Key": self.api_key}
        try:
            response = requests.get(f"{self.base_url}/api/v1/transactions/{transaction_id}", headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting transaction status from Another Bank: {str(e)}")
            return {"status": "error", "message": str(e)}

class ExampleACHSystem(ACHSystem):
    def __init__(self):
        self.ach_api_key = Config.EXAMPLE_ACH_API_KEY
        self.ach_base_url = Config.EXAMPLE_ACH_BASE_URL

    def process_ach_transaction(self, ach_data):
        headers = {"Authorization": f"Bearer {self.ach_api_key}"}
        try:
            response = requests.post(f"{self.ach_base_url}/ach", json=ach_data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error processing ACH transaction with Example ACH: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_ach_status(self, ach_id):
        headers = {"Authorization": f"Bearer {self.ach_api_key}"}
        try:
            response = requests.get(f"{self.ach_base_url}/ach/{ach_id}", headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting ACH status from Example ACH: {str(e)}")
            return {"status": "error", "message": str(e)}

class AnotherACHSystem(ACHSystem):
    def __init__(self):
        self.ach_api_key = Config.ANOTHER_ACH_API_KEY
        self.ach_base_url = Config.ANOTHER_ACH_BASE_URL

    def process_ach_transaction(self, ach_data):
        headers = {"X-ACH-API-Key": self.ach_api_key}
        try:
            response = requests.post(f"{self.ach_base_url}/v2/ach-transactions", json=ach_data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error processing ACH transaction with Another ACH: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_ach_status(self, ach_id):
        headers = {"X-ACH-API-Key": self.ach_api_key}
        try:
            response = requests.get(f"{self.ach_base_url}/v2/ach-transactions/{ach_id}", headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting ACH status from Another ACH: {str(e)}")
            return {"status": "error", "message": str(e)}

def get_bank_api(bank_name):
    bank_apis = {
        "example_bank": ExampleBankAPI,
        "another_bank": AnotherBankAPI,
        "mock_bank": MockBankAPI,
    }
    bank_api_class = bank_apis.get(bank_name)
    if bank_api_class:
        return bank_api_class()
    else:
        raise ValueError(f"Unsupported bank: {bank_name}")

def get_ach_system(ach_name):
    ach_systems = {
        "example_ach": ExampleACHSystem,
        "another_ach": AnotherACHSystem,
        "mock_ach": MockACHSystem,
    }
    ach_system_class = ach_systems.get(ach_name)
    if ach_system_class:
        return ach_system_class()
    else:
        raise ValueError(f"Unsupported ACH system: {ach_name}")
