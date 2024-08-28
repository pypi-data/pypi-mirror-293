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

from tpdk_safe_checkout.models.media import Media

class TestMedia(unittest.TestCase):
    """Media unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Media:
        """Test Media
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Media`
        """
        model = Media()
        if include_optional:
            return Media(
                id = 56,
                extension = '',
                filename = '',
                fingerprint = '',
                public_url = 'https://cdn.tripartie.app/b15e64db-fbd2-442b-afee-69ee45e2959b.jpg',
                file = bytes(b'blah'),
                b64_encoded_tmp_file = '',
                thumbnail = 'https://example.com/',
                original = 'https://example.com/',
                owner = 'https://example.com/',
                offers = [
                    'https://example.com/'
                    ],
                thumbnail_url = 'https://cdn.tripartie.app/b15e64db-fbd2-442b-afee-69ee45e2959b.jpg'
            )
        else:
            return Media(
                extension = '',
                filename = '',
                fingerprint = '',
                public_url = 'https://cdn.tripartie.app/b15e64db-fbd2-442b-afee-69ee45e2959b.jpg',
        )
        """

    def testMedia(self):
        """Test Media"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
