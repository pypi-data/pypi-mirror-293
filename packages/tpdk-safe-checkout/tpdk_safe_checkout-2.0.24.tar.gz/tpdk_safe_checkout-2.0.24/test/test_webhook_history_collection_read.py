# coding: utf-8

"""
    Safe Checkout

    Simple, yet elegant web interfaces for your convenience. One request away from your first secured C2C transaction.

    The version of the OpenAPI document: 2.0.24
    Contact: noc@tripartie.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from tpdk_safe_checkout.models.webhook_history_collection_read import WebhookHistoryCollectionRead

class TestWebhookHistoryCollectionRead(unittest.TestCase):
    """WebhookHistoryCollectionRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WebhookHistoryCollectionRead:
        """Test WebhookHistoryCollectionRead
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WebhookHistoryCollectionRead`
        """
        model = WebhookHistoryCollectionRead()
        if include_optional:
            return WebhookHistoryCollectionRead(
                id = 56,
                object_id = '',
                event = 'offer.transaction.authorized',
                response_code = 56,
                occurred_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                attempted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                retry_count = 56,
                in_progress = True
            )
        else:
            return WebhookHistoryCollectionRead(
                event = 'offer.transaction.authorized',
                occurred_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                retry_count = 56,
        )
        """

    def testWebhookHistoryCollectionRead(self):
        """Test WebhookHistoryCollectionRead"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
