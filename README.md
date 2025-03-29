# DeFiAid: AI-Powered Blockchain for Transparent Charitable Finance

**DeFiAid** (Decentralized Financial Aid) is a blockchain-powered charitable platform that ensures transparency, security, and efficiency in managing and distributing donations. Built on Ethereum and enhanced with AI-driven insights, DeFiAid integrates decentralized identity management, financial auditing, and real-time transaction tracking.

## Overview
DeFiAid supports:
- **Trustless Donations:** Ensuring transparent charitable transactions via smart contracts.
- **Decentralized Identity (DID):** Using **SelfKey SSID** for user identity verification.
- **Financial Transparency:** **Mandatory Audit Network (MAN)** for real-time audits.
- **ISO20022 Banking Integration:** Translating traditional bank transactions onto the Ethereum blockchain.

This platform bridges the gap between **traditional banking (ISO20022 standard)** and **decentralized finance (DeFi)** using AI-powered decision-making and secure blockchain technology.

---

## Key Features
✅ **ISO20022 Message Parsing & Conversion** (Seamless integration with banks)  
✅ **Multi-Bank API & ACH System Support**  
✅ **Ethereum Blockchain Integration** (Secured via Web3.py)  
✅ **Decentralized Smart Contracts for Fund Management**  
✅ **AI-Powered Fraud Detection & Decision Support**  
✅ **Centralized Dashboard for Monitoring Transactions**  

---

## Tech Stack
| Component       | Technology |
|---------------|------------|
| **Blockchain** | Ethereum, Solidity |
| **AI & ML**   | TensorFlow / PyTorch |
| **Backend**   | Flask, Web3.py |
| **Database**  | PostgreSQL |
| **Identity**  | SelfKey SSID |
| **APIs**      | Bank APIs, ACH Systems |

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/DeFiAid-Blockchain.git
cd DeFiAid-Blockchain
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file and add the required variables:
```env
DATABASE_URL=<Your_PostgreSQL_URL>
SECRET_KEY=<Your_Flask_Secret_Key>
ETHEREUM_NODE_URL=<Your_Ethereum_Node>
```
Also, set up **bank API keys** for transaction processing.

### 4. Initialize the Database
```bash
flask db upgrade
```

### 5. Run the Application
```bash
python main.py
```
Access the platform at **http://localhost:5000**

---

## Testing & Error Handling
Run the test suite to verify multi-bank API integration and error handling:
```bash
python test_multiple_apis.py
```
This ensures **robust logging**, **transaction verification**, and **error handling**.

---
