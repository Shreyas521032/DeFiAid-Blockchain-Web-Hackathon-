from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    custom_icon = db.Column(db.String(256))
    icon_position = db.Column(db.String(5), default='left')
    is_business = db.Column(db.Boolean, default=False)
    debit_cards = db.relationship('DebitCard', backref='user', lazy='dynamic')
    bank_accounts = db.relationship('BankAccount', backref='user', lazy='dynamic')
    business = db.relationship('Business', backref='owner', uselist=False)
    alerts = db.relationship('Alert', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_name = db.Column(db.String(128), nullable=False)
    business_address = db.Column(db.Text, nullable=False)
    business_phone = db.Column(db.String(20), nullable=False)
    business_email = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clients = db.relationship('Client', backref='business', lazy='dynamic')

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_since = db.Column(db.DateTime, default=datetime.utcnow)
    solvy_card = db.relationship('SolvyCard', backref='client', uselist=False)

class SolvyCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False, unique=True)
    expiration_date = db.Column(db.Date, nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount_threshold = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DebitCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    cardholder_name = db.Column(db.String(128), nullable=False)
    billing_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_number = db.Column(db.String(34), nullable=False)
    routing_number = db.Column(db.String(9), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    bank_name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    source_currency = db.Column(db.String(3), nullable=False)
    target_currency = db.Column(db.String(3), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    debtor_name = db.Column(db.String(128), nullable=False)
    creditor_name = db.Column(db.String(128), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
