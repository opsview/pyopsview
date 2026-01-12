# Copyright (C) 2003-2026 ITRS Group Ltd. All rights reserved

import pyopsview


CONFIG_HOST_ENDPOINT = 'https://server-1.net/rest/config/host'


def test_host_manager_list(request_mock, http_client, mocker):
    """
    Test that the HostManager.list method makes the expected API requests and
    returns the expected objects.
    """
    expected = request_mock.add_response(
        'GET', CONFIG_HOST_ENDPOINT, response_file='get_config_host.json'
    )
    host_manager = pyopsview.v2.config.hosts.HostManager(http_client)
    returned = list(host_manager.list())
    # Assert that we have the expected HTTP calls
    assert (
        mocker.call(
            url=CONFIG_HOST_ENDPOINT,
            method='GET',
            data=None,
            params={},
        )
        in request_mock.call_args_list
    )
    # Assert that the data has been decoded by the schema
    for returned_item, expected_item in zip(returned, expected['list']):
        assert returned_item == host_manager._schema.decode(expected_item)


def test_host_manager_find(request_mock, http_client, mocker):
    """
    Test that the HostManager.find method makes the expected API requests and
    returns the expected objects.
    """
    expected = request_mock.add_response(
        'GET', CONFIG_HOST_ENDPOINT, response_file='get_config_host_search.json'
    )
    host_manager = pyopsview.v2.config.hosts.HostManager(http_client)
    find_address = 'itrsgroup.com'
    returned = list(host_manager.find(address=find_address))
    # Assert that we have the expected HTTP calls
    assert (
        mocker.call(
            url=CONFIG_HOST_ENDPOINT,
            method='GET',
            data=None,
            params={'s.address': 'itrsgroup.com'},
        )
        in request_mock.call_args_list
    )
    # Assert that the data has been decoded by the schema
    for returned_item, expected_item in zip(returned, expected['list']):
        assert returned_item == host_manager._schema.decode(expected_item)


def test_host_manager_find_one(request_mock, http_client, mocker):
    """
    Test that the HostManager.find_one method makes the expected API requests
    and returns the expected object.
    """
    expected = request_mock.add_response(
        'GET', CONFIG_HOST_ENDPOINT, response_file='get_config_host.json'
    )
    host_manager = pyopsview.v2.config.hosts.HostManager(http_client)
    find_address = 'itrsgroup.com'
    returned_item = host_manager.find_one(address=find_address)
    # Assert that we have the expected HTTP calls
    assert (
        mocker.call(
            url=CONFIG_HOST_ENDPOINT,
            method='GET',
            data=None,
            params={'s.address': 'itrsgroup.com'},
        )
        in request_mock.call_args_list
    )
    # Assert that the data has been decoded by the schema
    assert returned_item == host_manager._schema.decode(expected['list'][0])


def test_host_manager_create(request_mock, http_client, mocker):
    """
    Test that the HostManager.create method makes the expected API requests and
    returns the expected objects.
    """
    expected = request_mock.add_response(
        'POST', CONFIG_HOST_ENDPOINT, response_file='post_config_host.json'
    )
    host_manager = pyopsview.v2.config.hosts.HostManager(http_client)
    returned_item = host_manager.create(
        name='newhost',
        address='localhost',
        monitored_by='Master Monitor Server',
        host_group='Monitor Servers',
    )
    # Assert that we have the expected HTTP calls
    assert (
        mocker.call(
            url=CONFIG_HOST_ENDPOINT,
            method='POST',
            data=mocker.ANY,  # Skip asserting for readability
            params=None,
        )
        in request_mock.call_args_list
    )
    # Assert that the data has been decoded by the schema
    assert returned_item == host_manager._schema.decode(expected['object'])


def test_host_manager_create_many(http_client, request_mock, mocker):
    """
    Test that the HostManager.create_many method makes the expected API
    requests and returns the expected objects.
    """
    request_mock.add_response(
        'POST', CONFIG_HOST_ENDPOINT, response={'objects_updated': '2'}
    )
    host_manager = pyopsview.v2.config.hosts.HostManager(http_client)
    returned_count = host_manager.create_many(
        [
            {
                'name': 'newhost_1',
                'address': 'itrsgroup.com',
                'monitored_by': 'Master Monitor Server',
                'host_group': 'Monitor Servers',
            },
            {
                'name': 'newhost_2',
                'address': 'opsview.com',
                'monitored_by': 'Master Monitor Server',
                'host_group': 'Monitor Servers',
            },
        ]
    )
    # Assert that we have the expected HTTP calls
    assert (
        mocker.call(
            url=CONFIG_HOST_ENDPOINT,
            method='POST',
            data=mocker.ANY,  # Skip asserting for readability
            params=None,
        )
        in request_mock.call_args_list
    )
    # Assert that the data has been decoded by the schema
    assert int(returned_count) == 2
