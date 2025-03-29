import requests
import json
import time

BASE_URL = "http://localhost:5000"

def login(username, password):
    response = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
    return response.cookies

def set_alert(cookies, amount_threshold, currency):
    data = {"amount_threshold": amount_threshold, "currency": currency}
    response = requests.post(f"{BASE_URL}/api/set_alert", json=data, cookies=cookies)
    return response.json()

def process_transaction(cookies, amount, currency, status, debtor_name, creditor_name, transaction_type):
    data = {
        "amount": amount,
        "currency": currency,
        "status": status,
        "debtor_name": debtor_name,
        "creditor_name": creditor_name,
        "transaction_type": transaction_type
    }
    response = requests.post(f"{BASE_URL}/api/transaction", json=data, cookies=cookies)
    return response.json()

if __name__ == "__main__":
    # Login
    cookies = login("testuser", "testpassword")

    # Set an alert
    alert_response = set_alert(cookies, 1000, "USD")
    print("Alert set response:", alert_response)

    # Process a transaction below the alert threshold
    transaction_response = process_transaction(cookies, 500, "USD", "completed", "John Doe", "Jane Smith", "transfer")
    print("Transaction below threshold response:", transaction_response)

    # Wait for a moment to allow real-time updates
    time.sleep(2)

    # Process a transaction above the alert threshold
    transaction_response = process_transaction(cookies, 1500, "USD", "completed", "Alice Johnson", "Bob Williams", "transfer")
    print("Transaction above threshold response:", transaction_response)

    print("Check the browser console for real-time updates and alert messages.")
