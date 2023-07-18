import pytest
from app import create_app

app = create_app()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    with app.app_context():
        yield


def test_register_url(client):
    data = {
        "ShortCode": 7000,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://example.com/confirmurl/",
        "ValidationURL": "https://example.com/validateurl/",
    }
    response = client.post('/c2b/register', data=data)
    assert response.status_code == 200


def test_process_payment_request_success(client):
    data = {
        'amount': 100,
        'tel_no': '254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/c2b/paybill', data=data)
    assert response.status_code == 200


def test_process_payment_request_invalid_amount(client):
    data = {
        'amount': -100,
        'tel_no': '254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/c2b/paybill', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid amount value'}


def test_process_payment_request_invalid_payment_type(client):
    data = {
        'amount': 100,
        'tel_no': '254712345678',
        'payment_type': 'BusinessPaymentgt',
        'occassion': 'Test Occasion'
    }
    response = client.post('/c2b/paybill', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid payment type'}


def test_process_payment_request_invalid_number(client):
    data = {
        'amount': 100,
        'tel_no': '+254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/c2b/paybill', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid phone number'}


def test_process_payment_request_missing_data(client):
    data = {
        'tel_no': '254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/c2b/paybill', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid amount value'}

    # Test missing tel_no
    data = {
        'amount': 100,
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/c2b/paybill', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid phone number'}

    # Test missing payment_type
    data = {
        'amount': 100,
        'tel_no': '254712345678',
        'occassion': 'Test Occasion'
    }
    response = client.post('/c2b/paybill', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid payment type'}
