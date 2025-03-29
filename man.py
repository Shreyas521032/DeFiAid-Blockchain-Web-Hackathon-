from bank_api_integration import get_ach_system
import logging
import traceback

logger = logging.getLogger(__name__)

def process_ach_transaction(parsed_data, ach_name):
    try:
        ach_system = get_ach_system(ach_name)
        ach_response = ach_system.process_ach_transaction(parsed_data)
        
        verification_result = verify_ach_transaction(parsed_data, ach_response)
        if not verification_result['success']:
            logger.error(f"ACH transaction verification failed: {verification_result['message']}")
            return {
                'error': f"ACH transaction verification failed: {verification_result['message']}",
                'details': verification_result
            }
        
        logger.info(f"ACH transaction processed successfully. ID: {ach_response.get('ach_id')}")
        return {'ach_response': ach_response}
    except ValueError as e:
        logger.error(f"Error processing ACH transaction: {str(e)}")
        return {'error': str(e), 'details': traceback.format_exc()}
    except Exception as e:
        logger.error(f"Unexpected error processing ACH transaction: {str(e)}")
        return {'error': f"Unexpected error: {str(e)}", 'details': traceback.format_exc()}

def verify_ach_transaction(parsed_data, ach_response):
    try:
        if not ach_response.get('ach_id'):
            return {'success': False, 'message': 'ACH ID is missing'}
        
        if parsed_data.get('amount') != ach_response.get('amount'):
            return {'success': False, 'message': 'Amount mismatch between parsed data and ACH response'}
        
        if parsed_data.get('currency') != ach_response.get('currency'):
            return {'success': False, 'message': 'Currency mismatch between parsed data and ACH response'}
        
        if ach_response.get('status') != 'completed':
            return {'success': False, 'message': f"Unexpected ACH transaction status: {ach_response.get('status')}"}
        
        # Verify debtor and creditor information
        if ach_response.get('debtor_name') != parsed_data.get('debtor_name') or \
           ach_response.get('creditor_name') != parsed_data.get('creditor_name'):
            return {'success': False, 'message': 'Debtor or creditor information mismatch'}
        
        # Verify transaction ID
        if ach_response.get('transaction_id') != parsed_data.get('transaction_id'):
            return {'success': False, 'message': 'Transaction ID mismatch'}
        
        # Add more verification checks as needed
        
        return {'success': True, 'message': 'ACH transaction verified successfully'}
    except Exception as e:
        logger.error(f"Error in verify_ach_transaction: {str(e)}")
        return {'success': False, 'message': f'ACH verification error: {str(e)}', 'details': traceback.format_exc()}
