import os
from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_socketio import SocketIO, emit
from models import db, User, Alert, Transaction
from werkzeug.security import check_password_hash
from decimal import Decimal, InvalidOperation
import logging
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.environ['PGUSER'], os.environ['PGPASSWORD'], os.environ['PGHOST'],
    os.environ['PGPORT'], os.environ['PGDATABASE']
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({'status': 'success', 'message': 'Logged in successfully'})
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})

@app.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', transactions=transactions)

@app.route('/api/set_alert', methods=['POST'])
@login_required
def set_alert():
    try:
        data = request.get_json()
        logger.info(f"Received alert data: {data}")
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        amount_threshold = data.get('amount_threshold')
        currency = data.get('currency')
        
        if not amount_threshold or not currency:
            logger.error("Missing amount_threshold or currency")
            return jsonify({'status': 'error', 'message': 'Missing amount_threshold or currency'}), 400
        
        try:
            amount_threshold = Decimal(str(amount_threshold))
        except InvalidOperation:
            logger.error(f"Invalid amount_threshold: {amount_threshold}")
            return jsonify({'status': 'error', 'message': 'Invalid amount_threshold'}), 400

        new_alert = Alert(user_id=current_user.id, amount_threshold=amount_threshold, currency=currency)
        db.session.add(new_alert)
        db.session.commit()
        
        logger.info(f"Alert set for user {current_user.id}: {amount_threshold} {currency}")
        
        return jsonify({'status': 'success', 'message': 'Alert set successfully'})
    except Exception as e:
        logger.error(f"Error setting alert: {str(e)}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'An error occurred while setting the alert'}), 500

def get_exchange_rate(source_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{source_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['rates'].get(target_currency)
    return None

@app.route('/api/transaction', methods=['POST'])
@login_required
def process_transaction():
    try:
        data = request.get_json()
        logger.info(f"Received transaction data: {data}")
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        amount = data.get('amount')
        source_currency = data.get('source_currency')
        target_currency = data.get('target_currency')
        status = data.get('status')
        debtor_name = data.get('debtor_name')
        creditor_name = data.get('creditor_name')
        transaction_type = data.get('transaction_type')
        
        if not all([amount, source_currency, target_currency, status, debtor_name, creditor_name, transaction_type]):
            logger.error("Missing required transaction fields")
            return jsonify({'status': 'error', 'message': 'Missing required transaction fields'}), 400
        
        try:
            amount = Decimal(str(amount))
        except InvalidOperation:
            logger.error(f"Invalid amount: {amount}")
            return jsonify({'status': 'error', 'message': 'Invalid amount'}), 400

        exchange_rate = get_exchange_rate(source_currency, target_currency)
        if not exchange_rate:
            logger.error(f"Failed to get exchange rate for {source_currency} to {target_currency}")
            return jsonify({'status': 'error', 'message': 'Failed to get exchange rate'}), 500

        new_transaction = Transaction(
            user_id=current_user.id,
            amount=float(amount),
            source_currency=source_currency,
            target_currency=target_currency,
            exchange_rate=exchange_rate,
            status=status,
            debtor_name=debtor_name,
            creditor_name=creditor_name,
            transaction_type=transaction_type
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        # Emit real-time update
        socketio.emit('transaction_update', {
            'id': new_transaction.id,
            'amount': str(new_transaction.amount),
            'source_currency': new_transaction.source_currency,
            'target_currency': new_transaction.target_currency,
            'exchange_rate': new_transaction.exchange_rate,
            'status': new_transaction.status,
            'debtor_name': new_transaction.debtor_name,
            'creditor_name': new_transaction.creditor_name,
            'timestamp': new_transaction.timestamp.isoformat()
        }, room=str(current_user.id))
        
        # Check alerts
        alerts = Alert.query.filter_by(user_id=current_user.id, currency=source_currency).all()
        for alert in alerts:
            if amount >= alert.amount_threshold:
                socketio.emit('alert_triggered', {
                    'message': f'Alert: Transaction amount {amount} {source_currency} exceeds threshold {alert.amount_threshold} {alert.currency}',
                    'transaction_id': new_transaction.id
                }, room=str(current_user.id))
        
        logger.info(f"Transaction processed successfully: ID {new_transaction.id}")
        return jsonify({'status': 'success', 'message': 'Transaction processed successfully', 'transaction_id': new_transaction.id})
    except Exception as e:
        logger.error(f"Error processing transaction: {str(e)}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'An error occurred while processing the transaction'}), 500

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        logger.info(f"User {current_user.id} connected")
        socketio.emit('connection_response', {'status': 'connected'}, room=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        logger.info(f"User {current_user.id} disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
