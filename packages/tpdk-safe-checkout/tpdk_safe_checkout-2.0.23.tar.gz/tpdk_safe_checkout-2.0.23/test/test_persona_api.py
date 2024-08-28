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

from tpdk_safe_checkout.api.persona_api import PersonaApi


class TestPersonaApi(unittest.TestCase):
    """PersonaApi unit test stubs"""

    def setUp(self) -> None:
        self.api = PersonaApi()

    def tearDown(self) -> None:
        pass

    def test_api_personas_get_collection(self) -> None:
        """Test case for api_personas_get_collection

        Retrieves the collection of Persona resources.
        """
        pass

    def test_api_personas_id_delete(self) -> None:
        """Test case for api_personas_id_delete

        Unregister a Persona (Your customer)
        """
        pass

    def test_api_personas_id_get(self) -> None:
        """Test case for api_personas_id_get

        Retrieves a Persona resource.
        """
        pass

    def test_api_personas_id_patch(self) -> None:
        """Test case for api_personas_id_patch

        Updates the Persona resource.
        """
        pass

    def test_api_personas_post(self) -> None:
        """Test case for api_personas_post

        Register a Persona (Your customer)
        """
        pass


if __name__ == '__main__':
    unittest.main()
