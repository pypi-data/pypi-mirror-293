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

from tpdk_safe_checkout.models.organization_collection_read import OrganizationCollectionRead

class TestOrganizationCollectionRead(unittest.TestCase):
    """OrganizationCollectionRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OrganizationCollectionRead:
        """Test OrganizationCollectionRead
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OrganizationCollectionRead`
        """
        model = OrganizationCollectionRead()
        if include_optional:
            return OrganizationCollectionRead(
                id = 56,
                name = '',
                vat_number = '',
                commercial_registry_number = '',
                website_url = '',
                icon = tpdk_safe_checkout.models.offer_media_read.Offer-Media-Read(
                    id = 56, 
                    public_url = 'https://cdn.tripartie.app/b15e64db-fbd2-442b-afee-69ee45e2959b.jpg', ),
                logo = tpdk_safe_checkout.models.offer_media_read.Offer-Media-Read(
                    id = 56, 
                    public_url = 'https://cdn.tripartie.app/b15e64db-fbd2-442b-afee-69ee45e2959b.jpg', )
            )
        else:
            return OrganizationCollectionRead(
        )
        """

    def testOrganizationCollectionRead(self):
        """Test OrganizationCollectionRead"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
