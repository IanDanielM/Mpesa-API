"""
STK Push Module

This module provides functionality for processing STK push requests and
handling callbacks.
"""
import logging
from datetime import datetime
from flask import Blueprint, request, Response, jsonify, current_app
from app.utils import make_request, get_password


stk = Blueprint('stk', __name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -'
                                               '%(message)s')


@stk.route('/stkpush/processrequest', methods=['GET', 'POST'])
def process_request() -> Response:
    """
    Process STK push request for mobile payment.

    This endpoint is used to initiate a Secure STK Push payment request for
    mobile payment.
    The STK (SIM Toolkit) push is a method to make payments on mobile devices.

    Parameters (sent via form data):
        amount (float): The amount to be paid.
        tel_no (str): The customer's phone number in the format 254XXXXXXXXX
        payment_type (str): The type of payment.Should be one of the following:
            - CustomerPayBillOnline
            - CustomerBuyGoodsOnline
        account_reference (str): The account reference for the transaction.
        description (str): A description of the transaction.

    Returns:
        Response: JSON response containing the STK push payment status and
        details.
    """
    url = current_app.config['BASE_URL'] + 'stkpush/v1/processrequest'
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    amount = request.form.get('amount', type=float)
    if amount is None or amount <= 0:
        return jsonify({"error": "Invalid amount value"})
    tel_no = request.form.get('tel_no', type=str)
    if tel_no is None or not tel_no.isdigit() or len(tel_no) < 10:
        return jsonify({"error": "Invalid phone number"})
    if tel_no.startswith('0'):
        tel_no = '254' + tel_no[1:]
    payment_type = request.form.get('payment_type', type=str)
    accepted_payment_types = ['CustomerPayBillOnline',
                              'CustomerBuyGoodsOnline']
    if payment_type not in accepted_payment_types:
        return jsonify({"error": "Invalid payment type"})
    account_reference = request.form.get('account_reference', type=str)
    description = request.form.get('description', type=str)
    data = {
        "BusinessShortCode": 174379,
        "Password": get_password(),
        "Timestamp": timestamp,
        "TransactionType": payment_type,
        "Amount": amount,
        "PartyA": tel_no,
        "PartyB": 174379,
        "PhoneNumber": tel_no,
        "CallBackURL": current_app.config['CALLBACK_URL'],
        "AccountReference": account_reference,
        "TransactionDesc": description
    }
    response = make_request(url, data)
    logging.info(data)
    return response


@stk.route('/stkpush/callback/', methods=['GET', 'POST'])
def callback() -> str:
    """
    Callback endpoint for STK push payment processing.

    This endpoint is used to receive the callback data from the mobile payment
    processing system.
    The mobile payment processing system sends the transaction details and
    status to this endpoint.

    Returns:
        Response: The raw data received via the callback request.
    """
    data = request.get_data().decode('utf-8')
    logging.info(data)
    return data


@stk.route('/stkpush/query/', methods=['GET', 'POST'])
def query_transaction() -> Response:
    """
    Query the status of a Transaction made through STK push.

    This endpoint is used to query the status of a transaction that was
    initiated using the STK push method.
    The function sends a request to the API to retrieve the current status of
    the transaction.

    Parameters (sent via form data):
        checkout_id (str): The unique identifier of the transaction
        (CheckoutRequestID).

    Returns:
        Response: JSON response containing the transaction status and
        details.
    """
    url = current_app.config['BASE_URL'] + 'stkpushquery/v1/query'
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    checkout_id = request.form.get('checkout_id', type=str)
    data = {
        "BusinessShortCode": current_app.config['SHORT_CODE'],
        "Password": get_password(),
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_id,
    }
    response = make_request(url, data)
    logging.info(data)
    return response
