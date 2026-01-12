# Copyright (C) 2003-2026 ITRS Group Ltd. All rights reserved

import pytest

import pyopsview.v2.client
import pyopsview.exceptions

from tests.conftest import get_test_client


def test_password_init(request_mock):
    """
    Test that creating a client using a password automatically fetches a token
    to use in subsequent requests.
    """
    http_client = get_test_client(
        request_mock,
        endpoint='https://server-1.net/rest/',
        username='user-1',
        password='password-1',
    )
    assert http_client.token == 'token-1'
    assert http_client._session.headers == {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Opsview-Username': 'user-1',
        'X-Opsview-Token': 'token-1',
    }


def test_token_init(request_mock):
    """
    Test that creating a client using a token use that token in subsequent
    requests.
    """
    http_client = get_test_client(
        request_mock,
        endpoint='https://server-1.net/rest/',
        username='user-1',
        token='token-X',
    )
    assert http_client.token == 'token-X'
    assert http_client._session.headers == {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Opsview-Username': 'user-1',
        'X-Opsview-Token': 'token-X',
    }


def test_missing_credentials():
    """
    Test that omitting a username, or a password or token raises an exception.
    """
    with pytest.raises(pyopsview.exceptions.OpsviewClientException):
        pyopsview.v2.client.Client(
            endpoint='https://server-1.net/rest/',
        )
    with pytest.raises(pyopsview.exceptions.OpsviewClientException):
        pyopsview.v2.client.Client(
            endpoint='https://server-1.net/rest/',
            username='user-1',
        )
    with pytest.raises(pyopsview.exceptions.OpsviewClientException):
        pyopsview.v2.client.Client(
            endpoint='https://server-1.net/rest/',
            password='password-1',
        )
    with pytest.raises(pyopsview.exceptions.OpsviewClientException):
        pyopsview.v2.client.Client(
            endpoint='https://server-1.net/rest/',
            token='token-1',
        )


def test_url_massaging(request_mock):
    """Test that we handle trailing slashes correctly."""
    assert (
        get_test_client(
            request_mock,
            endpoint='https://server-1.net/rest',
            username='user-1',
            token='token-1',
        ).base_url
        == 'https://server-1.net/rest/'
    )
    assert (
        get_test_client(
            request_mock,
            endpoint='https://server-1.net/',
            username='user-1',
            token='token-1',
        ).base_url
        == 'https://server-1.net/rest/'
    )
    assert (
        get_test_client(
            request_mock,
            endpoint='https://server-1.net',
            username='user-1',
            token='token-1',
        ).base_url
        == 'https://server-1.net/rest/'
    )


def test_version(request_mock, mocker):
    """
    Test that the version property works by doing the expected HTTP request to
    fetch the server version, and then caching it.
    """
    http_client = get_test_client(
        request_mock,
        endpoint='https://server-1.net/rest/',
        username='user-1',
        password='password-1',
    )
    assert http_client.version == '6.12.1'  # As mocked by get_test_client
    expected_request = mocker.call(
        url='https://server-1.net/rest/info', method='GET', data=None, params=None
    )
    assert expected_request in request_mock.call_args_list
    call_count = request_mock.call_count
    assert http_client.version == '6.12.1'  # Repeated access is cached
    assert request_mock.call_count == call_count


def test_status_code_exception(request_mock, http_client):
    """Test that a response with a bad status code raises an exception."""
    request_mock.add_response(
        'GET',
        'https://server-1.net/rest/foo',
        response='{"message": "403"}',
        status_code=403,
    )
    with pytest.raises(pyopsview.exceptions.OpsviewClientException) as excinfo:
        http_client.get('foo')
    assert '403' in str(excinfo.value)


@pytest.mark.parametrize(
    'client_method, kwargs, expected_endpoint, expected_http_method, expected_data, expected_params',
    [
        pytest.param(
            pyopsview.v2.Client.get,
            {'url': 'foo/bar'},
            'foo/bar',
            'GET',
            None,
            None,
            id='get',
        ),
        pytest.param(
            pyopsview.v2.Client.post,
            {'url': 'foo/bar', 'data': {'key': 'value'}},
            'foo/bar',
            'POST',
            '{"key": "value"}',
            None,
            id='post',
        ),
        pytest.param(
            pyopsview.v2.Client.put,
            {'url': 'foo/bar', 'data': {'key': 'value'}},
            'foo/bar',
            'PUT',
            '{"key": "value"}',
            None,
            id='put',
        ),
        pytest.param(
            pyopsview.v2.Client.delete,
            {'url': 'foo/bar'},
            'foo/bar',
            'DELETE',
            None,
            None,
            id='delete',
        ),
        pytest.param(
            pyopsview.v2.Client.reload,
            {},
            'reload',
            'POST',
            None,
            {},
            id='reload',
        ),
        pytest.param(
            pyopsview.v2.Client.reload,
            {'asynchronous': True},
            'reload',
            'POST',
            None,
            {'asynchronous': 1},
            id='reload-async',
        ),
        pytest.param(
            pyopsview.v2.Client.reload_status,
            {},
            'reload',
            'GET',
            None,
            None,
            id='reload_status',
        ),
        pytest.param(
            pyopsview.v2.Client.info,
            {},
            'info',
            'GET',
            None,
            None,
            id='info',
        ),
        pytest.param(
            pyopsview.v2.Client.server_info,
            {},
            'serverinfo',
            'GET',
            None,
            None,
            id='server_info',
        ),
        pytest.param(
            pyopsview.v2.Client.user_info,
            {},
            'user',
            'GET',
            None,
            None,
            id='user_info',
        ),
    ],
)
def test_client_methods(
    request_mock,
    mocker,
    client_method,
    kwargs,
    expected_endpoint,
    expected_http_method,
    expected_data,
    expected_params,
):
    """
    Test all the basic client shortcut methods by asserting that they result in
    the expected HTTP requests.
    """
    base_url = 'https://server-1.net/rest/'
    request_mock.add_response(
        expected_http_method,
        base_url + expected_endpoint,
        response='{"valid_json_but_not_used": 1}',
    )
    http_client = get_test_client(
        request_mock,
        endpoint=base_url,
        username='user-1',
        password='password-1',
    )
    client_method(http_client, **kwargs)
    expected_request = mocker.call(
        url=base_url + expected_endpoint,
        method=expected_http_method,
        data=expected_data,
        params=expected_params,
    )
    assert expected_request in request_mock.call_args_list


def test_multiple_clients(request_mock):
    """
    Test that we can create two client instances towards different endpoints.
    """
    request_mock.add_response(
        'POST',
        'https://server-1.net/rest/login',
        response={
            'token': 'token-1',
        },
    )
    request_mock.add_response(
        'POST',
        'https://server-2.net/rest/login',
        response={
            'token': 'token-2',
        },
    )
    mock_info = {
        'hosts_limit': '',
        'opsview_version': '6.12.1',
        'server_timezone_offset': '0',
        'opsview_edition': 'commercial',
        'uuid': '00000000-0000-0000-0000-000000000000',
        'opsview_build': '6.12.1.202601010457',
        'server_timezone': 'UTC',
    }
    request_mock.add_response(
        'GET',
        'https://server-1.net/rest/info',
        response=mock_info,
    )
    request_mock.add_response(
        'GET',
        'https://server-2.net/rest/info',
        response=mock_info,
    )
    client_1 = pyopsview.v2.client.Client(
        endpoint='https://server-1.net/rest/',
        username='user-1',
        password='password-1',
    )
    client_2 = pyopsview.v2.client.Client(
        endpoint='https://server-2.net/rest/',
        username='user-2',
        password='password-2',
    )
    assert client_1._session.headers == {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Opsview-Username': 'user-1',
        'X-Opsview-Token': 'token-1',
    }
    assert client_2._session.headers == {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Opsview-Username': 'user-2',
        'X-Opsview-Token': 'token-2',
    }
