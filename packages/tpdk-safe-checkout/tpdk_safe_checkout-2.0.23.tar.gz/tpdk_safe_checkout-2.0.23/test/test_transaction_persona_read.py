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

from tpdk_safe_checkout.models.transaction_persona_read import TransactionPersonaRead

class TestTransactionPersonaRead(unittest.TestCase):
    """TransactionPersonaRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TransactionPersonaRead:
        """Test TransactionPersonaRead
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TransactionPersonaRead`
        """
        model = TransactionPersonaRead()
        if include_optional:
            return TransactionPersonaRead(
                id = 56,
                first_name = 'John',
                last_name = 'Doe',
                language = 'fr',
                email = 'john.doe@gmail.com',
                mobile_phone_number = '+33745214529',
                address = tpdk_safe_checkout.models.transaction_address_read.Transaction-Address-Read(),
                registered = True
            )
        else:
            return TransactionPersonaRead(
        )
        """

    def testTransactionPersonaRead(self):
        """Test TransactionPersonaRead"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
