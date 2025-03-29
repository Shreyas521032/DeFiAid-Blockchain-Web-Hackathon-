import requests
import json

BASE_URL = "http://localhost:5000"

def send_iso20022_message(message_type, xml_data):
    url = f"{BASE_URL}/api/transaction"
    payload = json.dumps({"iso20022_data": xml_data})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)
    print(f"Response for {message_type}:")
    print(response.json())
    print("---")

# Existing test messages...

# New test messages for additional message types

customer_credit_transfer_initiation = """
<Document>
  <CstmrCdtTrfInitn>
    <PmtInf>
      <PmtId>
        <EndToEndId>E2E12345</EndToEndId>
      </PmtId>
      <ReqdExctnDt>2023-10-15</ReqdExctnDt>
      <Dbtr>
        <Nm>John Smith</Nm>
      </Dbtr>
      <DbtrAcct>
        <Id>
          <IBAN>GB29NWBK60161331926819</IBAN>
        </Id>
      </DbtrAcct>
      <CdtTrfTxInf>
        <Amt>
          <InstdAmt Ccy="EUR">1000.00</InstdAmt>
        </Amt>
        <Cdtr>
          <Nm>Jane Doe</Nm>
        </Cdtr>
        <CdtrAcct>
          <Id>
            <IBAN>DE89370400440532013000</IBAN>
          </Id>
        </CdtrAcct>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>
"""

customer_direct_debit_initiation = """
<Document>
  <CstmrDrctDbtInitn>
    <PmtInf>
      <PmtId>
        <EndToEndId>DD987654</EndToEndId>
      </PmtId>
      <ReqdColltnDt>2023-10-20</ReqdColltnDt>
      <Cdtr>
        <Nm>Energy Company</Nm>
      </Cdtr>
      <CdtrAcct>
        <Id>
          <IBAN>FR7630006000011234567890189</IBAN>
        </Id>
      </CdtrAcct>
      <DrctDbtTxInf>
        <PmtId>
          <EndToEndId>DD987654</EndToEndId>
        </PmtId>
        <InstdAmt Ccy="EUR">75.50</InstdAmt>
        <DrctDbtTx>
          <MndtRltdInf>
            <MndtId>MANDATE2023001</MndtId>
          </MndtRltdInf>
        </DrctDbtTx>
        <Dbtr>
          <Nm>Alice Johnson</Nm>
        </Dbtr>
        <DbtrAcct>
          <Id>
            <IBAN>IT60X0542811101000000123456</IBAN>
          </Id>
        </DbtrAcct>
      </DrctDbtTxInf>
    </PmtInf>
  </CstmrDrctDbtInitn>
</Document>
"""

customer_payment_status_report = """
<Document>
  <CstmrPmtStsRpt>
    <OrgnlGrpInfAndSts>
      <OrgnlMsgId>ORIGMSG123456</OrgnlMsgId>
      <OrgnlMsgNmId>pain.001.001.03</OrgnlMsgNmId>
      <GrpSts>ACCP</GrpSts>
    </OrgnlGrpInfAndSts>
    <OrgnlPmtInfAndSts>
      <TxInfAndSts>
        <OrgnlTxId>E2E12345</OrgnlTxId>
        <TxSts>ACCP</TxSts>
        <StsRsnInf>
          <Rsn>
            <Cd>AC01</Cd>
          </Rsn>
        </StsRsnInf>
      </TxInfAndSts>
    </OrgnlPmtInfAndSts>
  </CstmrPmtStsRpt>
</Document>
"""

if __name__ == "__main__":
    # Existing test cases...
    send_iso20022_message("Payment Status Report", payment_status_report)
    send_iso20022_message("Credit Transfer", credit_transfer)
    send_iso20022_message("Direct Debit", direct_debit)
    send_iso20022_message("Payment Return", payment_return)
    send_iso20022_message("Resolution of Investigation", resolution_of_investigation)
    send_iso20022_message("Bank to Customer Statement", bank_to_customer_statement)
    
    # New test cases
    send_iso20022_message("Customer Credit Transfer Initiation", customer_credit_transfer_initiation)
    send_iso20022_message("Customer Direct Debit Initiation", customer_direct_debit_initiation)
    send_iso20022_message("Customer Payment Status Report", customer_payment_status_report)
