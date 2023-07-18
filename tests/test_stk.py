import pytest
from app import create_app

app = create_app()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_process_request_success(client):
    data = {
        'amount': 100,
        'tel_no': '254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/stkpush/processrequest', data=data)
    assert response.status_code == 200


def test_query_transaction_success(client):
    data = {
        'checkout_id': 'ws_CO_1234567890123456789'
    }
    response = client.post('/stkpush/query/', data=data)
    assert response.status_code == 200


def test_process_request_invalid_amount(client):
    data = {
        'amount': -100,
        'tel_no': '254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/stkpush/processrequest', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid amount value'}


def test_process_request_invalid_payment_type(client):
    data = {
        'amount': 100,
        'tel_no': '254712345678',
        'payment_type': 'BusinessPaymentgt',
        'occassion': 'Test Occasion'
    }
    response = client.post('/stkpush/processrequest', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid payment type'}


def test_process_request_invalid_number(client):
    data = {
        'amount': 100,
        'tel_no': '+254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/stkpush/processrequest', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid phone number'}


def test_process_request_missing_data(client):
    data = {
        'tel_no': '254712345678',
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/stkpush/processrequest', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid amount value'}

    # Test missing tel_no
    data = {
        'amount': 100,
        'payment_type': 'BusinessPayment',
        'occassion': 'Test Occasion'
    }
    response = client.post('/stkpush/processrequest', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid phone number'}

    # Test missing payment_type
    data = {
        'amount': 100,
        'tel_no': '254712345678',
        'occassion': 'Test Occasion'
    }
    response = client.post('/stkpush/processrequest', data=data)
    assert response.status_code == 200
    assert response.json == {'error': 'Invalid payment type'}


def test_callback(client):
    data = '{"key": "value"}'
    response = client.post('/stkpush/callback/', data=data)
    assert response.status_code == 200
    assert response.data.decode('utf-8') == data
