# FLASK MPESA API

This is a sample wrapper providing access to Mpesa Daraja api for the modules C2B, B2C and M-Pesa express(STK-PUSH)

## Features

This repository only features the following APIs in Daraja:

- C2B:  Customer to Business (C2B) APIs and allows receiving payment notifications to your paybill
- B2C: B2C API is an API used to make payments from a Business to Customers
- M-Pesa Express (STK-PUSH): This API is a Merchant/Business initiated C2B (Customer to Business) Payment.

## Requirements

The requirements needed to run this application is:

- Python 3.10 + installed
- Mpesa Daraja API credentials from https://developer.safaricom.co.ke/

## Installation
To install this application you will need first to clone it you pc, create a virtual env and install requirements.txt

```bash
git clone https://github.com/IanDanielM/Flask-Mpesa-API.git
python -m venv venv
pip install -r requirements.txt
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

    ```env
    CONSUMER_KEY = 
    CONSUMER_SECRET = 
    PASSKEY = 
    SHORTCODE = 
    SECURITY_CREDENTIALS= 
    ```

## Configuration

configure your callback urls in the config.ini file

  ```ini
  [URLS]
  confirmurl = 
  validateurl = 
  timeouturl = 
  resulturl = 
  callbackurl = 
  ```

## Running Tests

To run tests, run the following command

```bash
pytest tests/
```

## Running the application

```bash
FLASK_APP=main.py FLASK_DEBUG=1 flask run
```
