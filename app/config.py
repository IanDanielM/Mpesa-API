"""
This module contains the configuration settings for the Mpesa Api

"""
import os
import configparser
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
config = configparser.ConfigParser()
config.read("/home/ian/MpesaApi/config.ini")


class Config:
    """
    application configuration
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    # api_base_url
    BASE_URL = " https://sandbox.safaricom.co.ke/mpesa/"

    # credentials
    CONSUMER_KEY = os.getenv('key')
    CONSUMER_SECRET = os.getenv('ConsumerSecret')
    SECURITY_CREDENTIALS = os.getenv("securitycredentials")
    PASSKEY = os.getenv("passkey")
    SHORT_CODE = os.getenv("shortcode")

    # url configurations
    CONFIRM_URL = config.get("URLS", "confirmurl")
    VALIDATE_URL = config.get("URLS", "validateurl")
    TIMEOUT_URL = config.get("URLS", "timeouturl")
    RESULT_URL = config.get("URLS", "resulturl")
    CALLBACK_URL = config.get("URLS", "callbackurl")
