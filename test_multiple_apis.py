import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:5000"

def test_transaction(iso20022_data, bank_name, ach_name):
    url = f"{BASE_URL}/api/transaction"
    payload = json.dumps({
        "iso20022_data": iso20022_data,
        "bank_name": bank_name,
        "ach_name": ach_name
    })
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        logger.info(f"Response for {bank_name} and {ach_name}:")
        logger.info(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending request: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {str(e)}")
    logger.info("---")

# Test data
iso20022_data = """
<Document>
  <FIToFIPmtStsRpt>
    <GrpHdr>
      <MsgId>MSGID/20231013/001</MsgId>
      <CreDtTm>2023-10-13T10:00:00</CreDtTm>
    </GrpHdr>
    <TxInfAndSts>
      <OrgnlTxId>TRX123456789</OrgnlTxId>
      <TxSts>ACCP</TxSts>
      <StsRsnInf>
        <Rsn>
          <Cd>AC01</Cd>
        </Rsn>
      </StsRsnInf>
      <OrgnlTxRef>
        <Amt>
          <InstdAmt Ccy="USD">1000.00</InstdAmt>
        </Amt>
        <Dbtr>
          <Nm>John Doe</Nm>
        </Dbtr>
        <DbtrAcct>
          <Id>
            <IBAN>US29NWBK60161331926819</IBAN>
          </Id>
        </DbtrAcct>
        <Cdtr>
          <Nm>Jane Smith</Nm>
        </Cdtr>
        <CdtrAcct>
          <Id>
            <IBAN>GB29NWBK60161331926819</IBAN>
          </Id>
        </CdtrAcct>
      </OrgnlTxRef>
    </TxInfAndSts>
  </FIToFIPmtStsRpt>
</Document>
"""

if __name__ == "__main__":
    # Test with mock bank and ACH
    test_transaction(iso20022_data, "mock_bank", "mock_ach")
    
    # Test with example bank and ACH
    test_transaction(iso20022_data, "example_bank", "example_ach")
    
    # Test with another bank and ACH
    test_transaction(iso20022_data, "another_bank", "another_ach")
    
    # Test with invalid bank name to check error handling
    test_transaction(iso20022_data, "invalid_bank", "mock_ach")
    
    # Test with invalid ISO20022 data to check error handling
    invalid_iso20022_data = "<InvalidDocument></InvalidDocument>"
    test_transaction(invalid_iso20022_data, "mock_bank", "mock_ach")
