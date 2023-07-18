"""
this module is used to create helper functions
"""
import base64
import logging
from datetime import datetime
from typing import Any
import requests
from requests.exceptions import RequestException, Timeout
from flask import jsonify, Response, current_app


BASE_URL = "https://sandbox.safaricom.co.ke/oauth/v1"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -'
                                               '%(message)s')


def get_access_token() -> str:
    """
    Fetches the access token from the server.

    Returns:
        str: The access token string.
    """
    if current_app.config['CONSUMER_KEY'] is None or \
            current_app.config['CONSUMER_SECRET'] is None:
        raise ValueError("Consumer key or consumer secret is missing.")
    key_secret = current_app.config['CONSUMER_KEY'] + ':' + current_app.config[
        'CONSUMER_SECRET']
    key_secret_bytes = key_secret.encode('ascii')
    base64_key_secret = base64.b64encode(key_secret_bytes)
    base64_key_secret_string = base64_key_secret.decode('ascii')
    url = BASE_URL + "/generate?grant_type=client_credentials"
    headers = {'Authorization': f'Basic {base64_key_secret_string}'}
    response_data = requests.get(url, headers=headers, timeout=30).json()
    token: str = response_data['access_token']
    return token


def get_password() -> str:
    """
    Generate and return a password for the STK push request.

    This function generates a password based on the current timestamp,
    shortcode, and passkey.
    If the shortcode or passkey is None, a ValueError is raised.
    The generated password is then encoded using base64 and returned as a
    string.

    Returns:
        str: The generated password for the STK push request.

    Raises:
        ValueError: If the shortcode or passkey is missing.
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    short_code = current_app.config['SHORT_CODE']
    passkey = current_app.config['PASSKEY']
    if short_code is None or passkey is None:
        raise ValueError("Consumer key or consumer secret is missing.")
    password = str(short_code) + passkey + timestamp
    password_bytes = base64.b64encode(password.encode('utf-8'))
    password_str = password_bytes.decode('utf-8')
    return password_str


def make_request(url: str, data: dict[str, Any]) -> Response:
    access_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.post(url, headers=headers, json=data,
                                 timeout=30).json()
        return jsonify(response)
    except (RequestException, Timeout) as request_error:
        logging.error("A request error occurred: %s", request_error)
        return jsonify({"error": str(request_error)})
