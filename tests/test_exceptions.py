# Copyright (C) 2003-2026 ITRS Group Ltd. All rights reserved

import pytest

import pyopsview.exceptions


@pytest.mark.parametrize(
    'response, message_startswith',
    [
        pytest.param(
            'foo',
            'foo',
            id='invalid',
        ),
        pytest.param(
            '{}',
            '\nTo include error detail in API responses',
            id='empty',
        ),
        pytest.param(
            '{"message": "Foo"}',
            'Opsview: "Foo"\nTo include error detail in API responses',
            id='message',
        ),
        pytest.param(
            '{"detail": "Bar"}',
            '\n\nDetail: "Bar"',
            id='detail',
        ),
        pytest.param(
            '{"message": "Foo", "detail": "Bar"}',
            'Opsview: "Foo"\n\nDetail: "Bar"',
            id='message-and-detail',
        ),
    ],
)
def test_opsview_client_exception(response, message_startswith):
    exc = pyopsview.exceptions.OpsviewClientException(response)
    assert str(exc).startswith(message_startswith)
