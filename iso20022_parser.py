import xmltodict
from typing import Dict, Any

def parse_iso20022(xml_data: str) -> Dict[str, Any]:
    """
    Parse ISO20022 XML data and extract relevant information.
    """
    try:
        parsed_data = xmltodict.parse(xml_data)
    except Exception as e:
        raise ValueError(f"Invalid XML data: {str(e)}")
    
    document = parsed_data.get('Document', {})
    if not document:
        raise ValueError("Invalid ISO20022 message: Missing Document element")
    
    root_element = list(document.keys())[0]
    
    parsers = {
        'FIToFIPmtStsRpt': parse_payment_status_report,
        'FIToFICstmrCdtTrf': parse_credit_transfer,
        'FIToFICstmrDrctDbt': parse_direct_debit,
        'PmtRtr': parse_payment_return,
        'RsltnOfInvstgtn': parse_resolution_of_investigation,
        'BkToCstmrStmt': parse_bank_to_customer_statement,
        'CstmrCdtTrfInitn': parse_customer_credit_transfer_initiation,
        'CstmrDrctDbtInitn': parse_customer_direct_debit_initiation,
        'CstmrPmtStsRpt': parse_customer_payment_status_report
    }
    
    parser = parsers.get(root_element)
    if parser:
        return parser(document[root_element])
    else:
        raise ValueError(f"Unsupported message type: {root_element}")

def parse_payment_status_report(data: Dict[str, Any]) -> Dict[str, Any]:
    transaction = data['TxInfAndSts']
    return {
        'message_type': 'payment_status_report',
        'transaction_id': transaction['OrgnlTxId'],
        'status': transaction['TxSts'],
        'reason': transaction.get('StsRsnInf', {}).get('Rsn', {}).get('Cd'),
        'amount': transaction['OrgnlTxRef']['Amt']['InstdAmt']['#text'],
        'currency': transaction['OrgnlTxRef']['Amt']['InstdAmt']['@Ccy'],
        'debtor_name': transaction['OrgnlTxRef']['Dbtr']['Nm'],
        'debtor_account': transaction['OrgnlTxRef']['DbtrAcct']['Id']['IBAN'],
        'creditor_name': transaction['OrgnlTxRef']['Cdtr']['Nm'],
        'creditor_account': transaction['OrgnlTxRef']['CdtrAcct']['Id']['IBAN'],
    }

def parse_credit_transfer(data: Dict[str, Any]) -> Dict[str, Any]:
    credit_transfer_info = data['CdtTrfTxInf']
    return {
        'message_type': 'credit_transfer',
        'transaction_id': credit_transfer_info['PmtId']['EndToEndId'],
        'amount': credit_transfer_info['IntrBkSttlmAmt']['#text'],
        'currency': credit_transfer_info['IntrBkSttlmAmt']['@Ccy'],
        'debtor_name': credit_transfer_info['Dbtr']['Nm'],
        'debtor_account': credit_transfer_info['DbtrAcct']['Id']['IBAN'],
        'creditor_name': credit_transfer_info['Cdtr']['Nm'],
        'creditor_account': credit_transfer_info['CdtrAcct']['Id']['IBAN'],
        'remittance_info': credit_transfer_info.get('RmtInf', {}).get('Ustrd'),
    }

def parse_direct_debit(data: Dict[str, Any]) -> Dict[str, Any]:
    direct_debit_info = data['DrctDbtTxInf']
    return {
        'message_type': 'direct_debit',
        'transaction_id': direct_debit_info['PmtId']['EndToEndId'],
        'amount': direct_debit_info['IntrBkSttlmAmt']['#text'],
        'currency': direct_debit_info['IntrBkSttlmAmt']['@Ccy'],
        'debtor_name': direct_debit_info['Dbtr']['Nm'],
        'debtor_account': direct_debit_info['DbtrAcct']['Id']['IBAN'],
        'creditor_name': direct_debit_info['Cdtr']['Nm'],
        'creditor_account': direct_debit_info['CdtrAcct']['Id']['IBAN'],
        'mandate_id': direct_debit_info['DrctDbtTx']['MndtRltdInf']['MndtId'],
    }

def parse_payment_return(data: Dict[str, Any]) -> Dict[str, Any]:
    return_info = data['TxInf']
    return {
        'message_type': 'payment_return',
        'transaction_id': return_info['RtrId'],
        'original_transaction_id': return_info['OrgnlTxId'],
        'amount': return_info['RtrdIntrBkSttlmAmt']['#text'],
        'currency': return_info['RtrdIntrBkSttlmAmt']['@Ccy'],
        'return_reason': return_info['RtrRsnInf']['Rsn']['Cd'],
    }

def parse_resolution_of_investigation(data: Dict[str, Any]) -> Dict[str, Any]:
    case_info = data['CaseAssgnmt']
    return {
        'message_type': 'resolution_of_investigation',
        'case_id': case_info['Id'],
        'creator': case_info['Cretr']['Pty']['Nm'],
        'status': data['Sts']['Conf'],
    }

def parse_bank_to_customer_statement(data: Dict[str, Any]) -> Dict[str, Any]:
    statement = data['Stmt']
    return {
        'message_type': 'bank_to_customer_statement',
        'account_id': statement['Acct']['Id']['IBAN'],
        'statement_id': statement['Id'],
        'creation_date_time': statement['CreDtTm'],
        'balance': statement['Bal'][0]['Amt']['#text'],
        'currency': statement['Bal'][0]['Amt']['@Ccy'],
    }

def parse_customer_credit_transfer_initiation(data: Dict[str, Any]) -> Dict[str, Any]:
    payment_info = data['PmtInf']
    credit_transfer_info = payment_info['CdtTrfTxInf']
    return {
        'message_type': 'customer_credit_transfer_initiation',
        'transaction_id': credit_transfer_info['PmtId']['EndToEndId'],
        'amount': credit_transfer_info['Amt']['InstdAmt']['#text'],
        'currency': credit_transfer_info['Amt']['InstdAmt']['@Ccy'],
        'debtor_name': payment_info['Dbtr']['Nm'],
        'debtor_account': payment_info['DbtrAcct']['Id']['IBAN'],
        'creditor_name': credit_transfer_info['Cdtr']['Nm'],
        'creditor_account': credit_transfer_info['CdtrAcct']['Id']['IBAN'],
        'requested_execution_date': payment_info['ReqdExctnDt'],
    }

def parse_customer_direct_debit_initiation(data: Dict[str, Any]) -> Dict[str, Any]:
    payment_info = data['PmtInf']
    direct_debit_info = payment_info['DrctDbtTxInf']
    return {
        'message_type': 'customer_direct_debit_initiation',
        'transaction_id': direct_debit_info['PmtId']['EndToEndId'],
        'amount': direct_debit_info['InstdAmt']['#text'],
        'currency': direct_debit_info['InstdAmt']['@Ccy'],
        'debtor_name': direct_debit_info['Dbtr']['Nm'],
        'debtor_account': direct_debit_info['DbtrAcct']['Id']['IBAN'],
        'creditor_name': payment_info['Cdtr']['Nm'],
        'creditor_account': payment_info['CdtrAcct']['Id']['IBAN'],
        'mandate_id': direct_debit_info['DrctDbtTx']['MndtRltdInf']['MndtId'],
        'requested_collection_date': payment_info['ReqdColltnDt'],
    }

def parse_customer_payment_status_report(data: Dict[str, Any]) -> Dict[str, Any]:
    original_group_info = data['OrgnlGrpInfAndSts']
    transaction_info = data['OrgnlPmtInfAndSts']['TxInfAndSts']
    return {
        'message_type': 'customer_payment_status_report',
        'original_message_id': original_group_info['OrgnlMsgId'],
        'original_message_type': original_group_info['OrgnlMsgNmId'],
        'group_status': original_group_info.get('GrpSts'),
        'transaction_id': transaction_info['OrgnlTxId'],
        'transaction_status': transaction_info['TxSts'],
        'status_reason': transaction_info.get('StsRsnInf', {}).get('Rsn', {}).get('Cd'),
    }
