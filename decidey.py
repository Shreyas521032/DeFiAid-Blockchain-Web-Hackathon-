from bank_api_integration import get_bank_api
from ethereum_integration import translate_to_ethereum, store_on_blockchain
import logging
import traceback

logger = logging.getLogger(__name__)

def process_transaction(parsed_data, bank_name):
    try:
        bank_api = get_bank_api(bank_name)
        bank_response = bank_api.send_transaction(parsed_data)
        
        if bank_response.get("status") == "error":
            logger.error(f"Error from bank API: {bank_response.get('message')}")
            return {
                'error': f"Bank API error: {bank_response.get('message')}",
                'details': bank_response
            }
        
        ethereum_data = translate_to_ethereum(parsed_data)
        transaction_hash = store_on_blockchain(ethereum_data)
        
        verification_result = verify_transaction(bank_response, ethereum_data, transaction_hash, parsed_data)
        if not verification_result['success']:
            logger.error(f"Transaction verification failed: {verification_result['message']}")
            return {
                'error': f"Transaction verification failed: {verification_result['message']}",
                'details': verification_result
            }
        
        logger.info(f"Transaction processed successfully. Hash: {transaction_hash}")
        return {
            'bank_response': bank_response,
            'ethereum_data': ethereum_data,
            'transaction_hash': transaction_hash
        }
    except Exception as e:
        logger.error(f"Error in process_transaction: {str(e)}")
        return {
            'error': f"Unexpected error in process_transaction: {str(e)}",
            'details': traceback.format_exc()
        }

def verify_transaction(bank_response, ethereum_data, transaction_hash, parsed_data):
    try:
        if not transaction_hash:
            return {'success': False, 'message': 'Transaction hash is missing'}
        
        if bank_response.get('amount') != ethereum_data.get('amount'):
            return {'success': False, 'message': 'Amount mismatch between bank and Ethereum data'}
        
        if bank_response.get('currency') != parsed_data.get('currency'):
            return {'success': False, 'message': 'Currency mismatch between bank response and parsed data'}
        
        if bank_response.get('status') != 'completed':
            return {'success': False, 'message': f"Unexpected transaction status: {bank_response.get('status')}"}
        
        # Verify debtor and creditor information
        if bank_response.get('debtor_name') != parsed_data.get('debtor_name') or \
           bank_response.get('creditor_name') != parsed_data.get('creditor_name'):
            return {'success': False, 'message': 'Debtor or creditor information mismatch'}
        
        # Verify transaction ID
        if bank_response.get('transaction_id') != parsed_data.get('transaction_id'):
            return {'success': False, 'message': 'Transaction ID mismatch'}
        
        # Add more verification checks as needed
        
        return {'success': True, 'message': 'Transaction verified successfully'}
    except Exception as e:
        logger.error(f"Error in verify_transaction: {str(e)}")
        return {'success': False, 'message': f'Verification error: {str(e)}', 'details': traceback.format_exc()}
