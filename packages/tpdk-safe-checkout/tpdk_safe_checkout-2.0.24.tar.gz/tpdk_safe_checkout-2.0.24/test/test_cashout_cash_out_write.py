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

from tpdk_safe_checkout.models.cashout_cash_out_write import CashoutCashOutWrite

class TestCashoutCashOutWrite(unittest.TestCase):
    """CashoutCashOutWrite unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CashoutCashOutWrite:
        """Test CashoutCashOutWrite
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CashoutCashOutWrite`
        """
        model = CashoutCashOutWrite()
        if include_optional:
            return CashoutCashOutWrite(
                captcha = ''
            )
        else:
            return CashoutCashOutWrite(
        )
        """

    def testCashoutCashOutWrite(self):
        """Test CashoutCashOutWrite"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
