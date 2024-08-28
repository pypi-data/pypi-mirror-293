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

from tpdk_safe_checkout.models.user_write import UserWrite

class TestUserWrite(unittest.TestCase):
    """UserWrite unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UserWrite:
        """Test UserWrite
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UserWrite`
        """
        model = UserWrite()
        if include_optional:
            return UserWrite(
                captcha = '',
                first_name = 'Jacob',
                last_name = 'TAHRI',
                public_name = 'Nickname',
                role_in_company = 'Accounting Dpt',
                birthday = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                email = 'john.doe@company.tld',
                plain_password = 'secr$t',
                intl_phone_number = '+33700000000',
                origin_country = 'FRA',
                home_country = 'FRA',
                preferred_language = 'fr',
                consent_mail_ads = True
            )
        else:
            return UserWrite(
                captcha = '',
                first_name = 'Jacob',
                last_name = 'TAHRI',
                email = 'john.doe@company.tld',
                plain_password = 'secr$t',
        )
        """

    def testUserWrite(self):
        """Test UserWrite"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
