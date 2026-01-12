# Copyright (C) 2003-2026 ITRS Group Ltd. All rights reserved

import json
import pathlib

import pytest

import pyopsview


RESOURCE_DIR = pathlib.Path(__file__).parent / 'mock_responses'


@pytest.fixture(scope='function')
def request_mock(mocker):
    """
    This fixture mocks the requests module used by pyopsview so that it creates
    a Mock instead of an actual requests Session, to prevent any real network
    calls from happening. The mocked Session instead returns predefined
    response data when its request method is called. These responses can be
    predefined via the request_mock.add_response function.
    """

    mock_responses = {}

    def add_response(method, url, response=None, response_file=None, status_code=200):
        if (response is None) is (response_file is None):
            raise TypeError(
                'add_response expected either one of response or response_file to be set'
            )
        if response_file:
            response_json = (RESOURCE_DIR / response_file).read_text()
            response_data = json.loads(response_json)
        elif isinstance(response, str):
            response_json = response
            response_data = json.loads(response)
        else:
            # Allow use of native Python types in mocked responses, convert to
            # JSON to mimic an actual API response.
            response_data = response
            response_json = json.dumps(response)
        mock_responses[(method, url)] = (status_code, response_json)
        return response_data

    def request(method, url, **kwargs):
        try:
            status_code, response_json = mock_responses[(method, url)]
        except KeyError:
            raise RuntimeError(f'request_mock has no response for: {method} {url}')
        return mocker.Mock(
            encoding='utf-8',
            status_code=status_code,
            text=response_json,
        )

    request_mock = mocker.Mock(side_effect=request, add_response=add_response)

    mocker.patch.object(
        pyopsview.v2.client,
        'requests',
        mocker.Mock(
            session=mocker.Mock(side_effect=lambda: mocker.Mock(request=request_mock))
        ),
    )

    yield request_mock


@pytest.fixture
def http_client(request_mock):
    """
    This fixture yields a pyopsview Client with basic dummy configuration.
    """
    yield get_test_client(
        request_mock,
        endpoint='https://server-1.net/rest/',
        username='user-1',
        password='password-1',
        strict=True,
    )


def get_test_client(request_mock, *args, **kwargs):
    """
    Return a pyopsview Client with the provided parameters. All initial API
    calls made by the client are mocked.
    """
    endpoint = kwargs['endpoint'].strip('/')
    request_mock.add_response(
        'POST',
        f'{endpoint}/login',
        response={
            'token': 'token-1',
        },
    )
    request_mock.add_response(
        'GET',
        f'{endpoint}/info',
        response={
            'hosts_limit': '',
            'opsview_version': '6.12.1',
            'server_timezone_offset': '0',
            'opsview_edition': 'commercial',
            'uuid': '11111111-1111-1111-1111-111111111111',
            'opsview_build': '6.12.1.202601010457',
            'server_timezone': 'UTC',
        },
    )
    return pyopsview.v2.client.Client(*args, **kwargs)
