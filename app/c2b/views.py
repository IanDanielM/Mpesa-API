"""
C2B Module

This module provides endpoints for registering URLs and handling
payment transactions for the C2B payment API.

The C2B payment API allows customers to make payments via Paybill or till
number
"""
import logging
from flask import Blueprint, request, jsonify, Response, current_app
from app.utils import make_request


c2b = Blueprint('c2b', __name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -'
                                               '%(message)s')


@c2b.route('/c2b/register', methods=['GET', 'POST'])
def register_url() -> Response:
    """
    Register URL for C2B (Consumer to Business) payment API.

    This endpoint is used to register the confirmation and validation URLs for
    C2B payments.
    The registered URLs are used by the API to notify the server about payment
    status and perform validation.

    Parameters:
        None (The required data is pre-defined in the function)

    Returns:
        Response: JSON response containing the registration status and
        details.
    """

    url = current_app.config['BASE_URL'] + 'c2b/v1/registerurl'
    data = {
        "ShortCode": 600996,
        "ResponseType": "Completed",
        "ConfirmationURL": current_app.config['CONFIRM_URL'],
        "ValidationURL": current_app.config['VALIDATE_URL'],
    }
    response = make_request(url, data)
    return response


@c2b.route('/c2b/validate/')
def validate_url() -> str:
    """
    This endpoint receives and logs the data sent via a POST request.
    This is typically used to validate the payment URL before processing
    the payment.

    Parameters:
        None (The data is received via the request body)

    Returns:
        Response: The raw data received via the POST request.

    """
    data = request.get_data().decode('utf-8')
    logging.info(data)
    return data


@c2b.route('/c2b/confirmation/')
def confirm_url() -> str:
    """
    This endpoint receives and logs the data sent via a POST request.
    This is typically used to confirm the successful completion of a payment
    after processing.

    Parameters:
        - None (The data is received via the request body)

    Returns:
        - Response: The raw data received via the POST request.
    """
    data = request.get_data().decode('utf-8')
    logging.info(data)
    return data


@c2b.route('/c2b/paybill', methods=['GET', 'POST'])
def paybill() -> Response:
    """
    route for the C2B (Consumer to Business) payment API.

    This route handles payment transactions for the specified payment types:
    - CustomerPayBillOnline
    - CustomerBuyGoodsOnline

    Parameters (sent via form data):
        amount (float): The amount to be paid.
        tel_no (str): The customer's phone number in the format 254XXXXXXXXX
        payment_type (str): The type of payment.Should be one of the following:
            - 'CustomerPayBillOnline'
            - 'CustomerBuyGoodsOnline'
        bill_reference (str): Required for 'CustomerPayBillOnline' payment
        type, the bill reference number.

    Returns:
        Response: JSON response containing payment status and details.
    """
    try:
        url = current_app.config['BASE_URL'] + 'c2b/v1/simulate'
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
        bill_reference = request.form.get('bill_reference', type=str)
        if payment_type == 'CustomerPayBillOnline' and (
                bill_reference is None or bill_reference.strip() == ""):
            return jsonify({"error": "Bill reference is required for"
                                     "CustomerPayBillOnline payment type"})
        data = {
            "ShortCode": 600992,
            "CommandID": payment_type,
            "Amount": amount,
            "Msisdn": tel_no,
            "BillRefNumber": bill_reference
        }
        response = make_request(url, data)
        return response
    except (KeyError, AttributeError, TypeError) as error:
        logging.error('An error occurred %s', error)
        return jsonify({"error": "An error occurred while processing your "
                                 "request."})
