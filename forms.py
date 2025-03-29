from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class ExistingAccountForm(FlaskForm):
    account_number = StringField('Account Number', validators=[DataRequired(), Length(min=4, max=34)])
    routing_number = StringField('Routing Number', validators=[DataRequired(), Length(9), Regexp(r'^\d{9}$', message='Routing number must be 9 digits')])
    account_type = SelectField('Account Type', choices=[('checking', 'Checking'), ('savings', 'Savings')], validators=[DataRequired()])
    bank_name = StringField('Bank Name', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Add Account')

class ExistingCardForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired(), Length(16), Regexp(r'^\d{16}$', message='Card number must be 16 digits')])
    expiration_date = DateField('Expiration Date', format='%Y-%m', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired(), Length(3), Regexp(r'^\d{3}$', message='CVV must be 3 digits')])
    cardholder_name = StringField('Cardholder Name', validators=[DataRequired(), Length(max=128)])
    billing_address = StringField('Billing Address', validators=[DataRequired()])
    submit = SubmitField('Add Card')
