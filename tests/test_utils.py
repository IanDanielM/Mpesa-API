from unittest.mock import patch
import pytest
from requests.exceptions import RequestException
from flask import current_app
from app import create_app
from app.utils import get_password, get_access_token, make_request


app = create_app()


@pytest.fixture
def app_context():
    with app.app_context():
        yield


def test_get_password(app_context):
    password = get_password()
    assert isinstance(password, str)
    assert len(password) > 0


def test_get_password_errors(app_context, monkeypatch):
    monkeypatch.setitem(current_app.config, 'SHORT_CODE', None)
    monkeypatch.setitem(current_app.config, 'PASSKEY', 'passkey')
    with pytest.raises(ValueError):
        get_password()
    monkeypatch.setitem(current_app.config, 'SHORT_CODE', 'shortcode')
    monkeypatch.setitem(current_app.config, 'PASSKEY', None)
    with pytest.raises(ValueError):
        get_password()


def test_get_access_token(app_context):
    access_token = get_access_token()
    assert isinstance(access_token, str)
    assert len(access_token) > 0


def test_get_access_token_errors(app_context, monkeypatch):
    monkeypatch.setitem(current_app.config, 'CONSUMER_KEY', None)
    monkeypatch.setitem(current_app.config, 'CONSUMER_SECRET', 'consumer_secret')

    with pytest.raises(ValueError):
        get_access_token()

    monkeypatch.setitem(current_app.config, 'CONSUMER_KEY', 'consumer_key')
    monkeypatch.setitem(current_app.config, 'CONSUMER_SECRET', None)

    with pytest.raises(ValueError):
        get_access_token()


def test_make_request_success(app_context):
    url = 'https://example.com'
    data = {'key': 'value'}
    expected_response = {'success': True}

    with patch('app.utils.requests.post') as mock_post:
        mock_post.return_value.json.return_value = expected_response
        response = make_request(url, data)
        assert response.json == expected_response


def test_make_request_error(app_context):
    url = 'https://example.com'
    data = {'key': 'value'}
    expected_error = 'An error occurred'

    with patch('app.utils.requests.post') as mock_post:
        mock_post.side_effect = RequestException(expected_error)
        response = make_request(url, data)
        assert response.json == {'error': expected_error}
