# coding: utf-8

"""
    Safe Checkout

    Simple, yet elegant web interfaces for your convenience. One request away from your first secured C2C transaction.

    The version of the OpenAPI document: 2.0.23
    Contact: noc@tripartie.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from tpdk_safe_checkout.models.webhook_history_read import WebhookHistoryRead

class TestWebhookHistoryRead(unittest.TestCase):
    """WebhookHistoryRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WebhookHistoryRead:
        """Test WebhookHistoryRead
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WebhookHistoryRead`
        """
        model = WebhookHistoryRead()
        if include_optional:
            return WebhookHistoryRead(
                id = 56,
                object_id = '',
                event = 'offer.transaction.authorized',
                url = '',
                normalized_object = [
                    ''
                    ],
                response_code = 56,
                response_body = '',
                occurred_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                attempted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                retry_count = 56,
                in_progress = True
            )
        else:
            return WebhookHistoryRead(
                event = 'offer.transaction.authorized',
                url = '',
                occurred_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                retry_count = 56,
        )
        """

    def testWebhookHistoryRead(self):
        """Test WebhookHistoryRead"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
