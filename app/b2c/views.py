"""
B2C Module
This module provides functionality for processing B2C payment requests
and handling related callbacks.
"""
import logging
from flask import Blueprint, request, jsonify, Response, current_app
from app.utils import make_request


b2c = Blueprint('b2c', __name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -'
                                               '%(message)s')


@b2c.route('/')
def index() -> str:
    """Wrapper for Mpesa API"""
    return "<p>Mpesa Playground</p>"


@b2c.route('/b2c/paymentrequest', methods=['GET', 'POST'])
def process_payment_request() -> Response:
    """
    Process B2C (Business to Customer) payment request.

    This endpoint is used to initiate a B2C payment request, where a business
    makes a payment to a customer.
    The function sends a request to the API to process the payment.

    Parameters (sent via form data):
        amount (float): The amount to be paid.
        tel_no (str): The customer's phone number in the format 254XXXXXXXXX
        payment_type (str): The type of payment.Should be one of the following:
            - BusinessPayment
            - SalaryPayment
            - PromotionPayment
        occassion (str): The reason for the payment or a unique identifier
        for the transaction.

    Returns:
        Response: JSON response containing the B2C payment status and details.
    """
    url = current_app.config['BASE_URL'] + 'b2c/v1/paymentrequest'
    amount = request.form.get('amount', type=float)
    if amount is None or amount <= 0:
        return jsonify({"error": "Invalid amount value"})
    tel_no = request.form.get('tel_no', type=str)
    if tel_no is None or not tel_no.isdigit() or len(tel_no) < 10:
        return jsonify({"error": "Invalid phone number"})
    if tel_no.startswith('0'):
        tel_no = '254' + tel_no[1:]
    payment_type = request.form.get('payment_type', type=str)
    accepted_payment_types = ['BusinessPayment', 'SalaryPayment',
                              'PromotionPayment']
    if payment_type not in accepted_payment_types:
        return jsonify({"error": "Invalid payment type"})
    occassion = request.form.get('occassion', type=str)
    data = {
        "InitiatorName": "testapi",
        "SecurityCredential": current_app.config['SECURITY_CREDENTIALS'],
        "CommandID": "SalaryPayment",
        "Amount": amount,
        "PartyA": 600986,
        "PartyB": tel_no,
        "Remarks": "Test remarks",
        "QueueTimeOutURL": current_app.config['TIMEOUT_URL'],
        "ResultURL": current_app.config['RESULT_URL'],
        "Occassion": occassion,
    }

    response = make_request(url, data)
    return response


@b2c.route('/b2c/result', methods=['GET', 'POST'])
def get_result() -> str:
    """
    This endpoint is used to receive and store the result of a B2C transaction.
    The B2C payment processing system sends the result of the transaction to
    this endpoint.

    Returns:
        str: The received data in JSON format.
    """
    data = request.get_data().decode('utf-8')
    logging.info(data)
    return data


@b2c.route('/b2c/queue', methods=['GET', 'POST'])
def get_queue() -> str:
    """
    This endpoint is used to receive and store the timeout response of a B2C
    transaction.
    If the payment processing system does not receive a response to the B2C
    request within the specified timeout period, it sends a timeout response
    to this endpoint.

    Returns:
        str: The received data in JSON format.
    """
    data = request.get_data().decode('utf-8')
    logging.info(data)
    return data
