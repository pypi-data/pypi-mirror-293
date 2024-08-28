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

from tpdk_safe_checkout.models.invalid_query_error import InvalidQueryError

class TestInvalidQueryError(unittest.TestCase):
    """InvalidQueryError unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> InvalidQueryError:
        """Test InvalidQueryError
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `InvalidQueryError`
        """
        model = InvalidQueryError()
        if include_optional:
            return InvalidQueryError(
                type = 'https://tools.ietf.org/html/rfc2616#section-10',
                title = 'An error occurred',
                detail = 'The request is malformed and therefore cannot be executed'
            )
        else:
            return InvalidQueryError(
        )
        """

    def testInvalidQueryError(self):
        """Test InvalidQueryError"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
