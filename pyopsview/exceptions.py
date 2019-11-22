#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from pyopsview.utils import json


class OpsviewClientException(Exception):
    """Base exception for all opsview client exceptions.

    Takes a `response` and attempts to extract the error detail. If JSON
    decoding fails, the original (possibly encoded) text is used..

    If no error detail is present in the response, details of how to enable
    response details in Opsview Web are used.
    """
    def __init__(self, response):
        try:
            response_decoded = json.loads(response)
        except (KeyError, ValueError):
            super(OpsviewClientException, self).__init__(response)
        else:
            if 'message' in response_decoded:
                message = 'Opsview: "{}"'.format(response_decoded['message'])
            else:
                message = ""

            if 'detail' in response_decoded:
                detail = '\nDetail: "{}"'.format(response_decoded['detail'])
            else:
                detail = ("To include error detail in API responses, set "
                          "'ControllerBase::Rest: {include_error_detail: 1}' "
                          "in opsview_web_local.yml")

            super(OpsviewClientException, self).__init__(
                '\n'.join([message, detail])
            )
