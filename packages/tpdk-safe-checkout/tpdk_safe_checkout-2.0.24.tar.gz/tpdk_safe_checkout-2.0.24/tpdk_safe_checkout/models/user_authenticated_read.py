# coding: utf-8

"""
    Safe Checkout

    Simple, yet elegant web interfaces for your convenience. One request away from your first secured C2C transaction.

    The version of the OpenAPI document: 2.0.24
    Contact: noc@tripartie.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tpdk_safe_checkout.models.user_bank_account_authenticated_read import UserBankAccountAuthenticatedRead
from tpdk_safe_checkout.models.user_card_authenticated_read import UserCardAuthenticatedRead
from tpdk_safe_checkout.models.user_media_authenticated_read import UserMediaAuthenticatedRead
from tpdk_safe_checkout.models.user_organization_authenticated_read import UserOrganizationAuthenticatedRead
from tpdk_safe_checkout.models.user_persona_authenticated_read import UserPersonaAuthenticatedRead
from tpdk_safe_checkout.models.user_wallet_authenticated_read import UserWalletAuthenticatedRead
from typing import Optional, Set
from typing_extensions import Self

class UserAuthenticatedRead(BaseModel):
    """
    
    """ # noqa: E501
    id: Optional[StrictInt] = None
    main_address: Optional[Dict[str, Any]] = Field(default=None, alias="mainAddress")
    first_name: Optional[StrictStr] = Field(default=None, alias="firstName")
    last_name: Optional[StrictStr] = Field(default=None, alias="lastName")
    public_name: Optional[StrictStr] = Field(default=None, alias="publicName")
    role_in_company: Optional[StrictStr] = Field(default=None, alias="roleInCompany")
    birthday: Optional[datetime] = None
    email: Optional[StrictStr] = None
    roles: List[StrictStr]
    totp_enabled: Optional[StrictBool] = Field(default=None, alias="totpEnabled")
    intl_phone_number: Optional[StrictStr] = Field(default=None, alias="intlPhoneNumber")
    origin_country: Optional[Annotated[str, Field(strict=True, max_length=3)]] = Field(default=None, description="The nationality of the current user.", alias="originCountry")
    home_country: Optional[Annotated[str, Field(strict=True, max_length=3)]] = Field(default=None, description="The originating country", alias="homeCountry")
    preferred_language: Optional[Annotated[str, Field(strict=True, max_length=2)]] = Field(default=None, alias="preferredLanguage")
    last_successful_log_in: Optional[datetime] = Field(default=None, alias="lastSuccessfulLogIn")
    avatar: Optional[UserMediaAuthenticatedRead] = None
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")
    consent_mail_ads: StrictBool = Field(alias="consentMailAds")
    lockdown: StrictBool
    organization: Optional[UserOrganizationAuthenticatedRead] = None
    bank_account: Optional[UserBankAccountAuthenticatedRead] = Field(default=None, alias="bankAccount")
    identity_verified_at: Optional[datetime] = Field(default=None, alias="identityVerifiedAt")
    profiles: List[UserPersonaAuthenticatedRead]
    cards: Optional[List[UserCardAuthenticatedRead]] = None
    wallet: Optional[UserWalletAuthenticatedRead] = None
    provider_name: Optional[StrictStr] = Field(default=None, alias="providerName")
    provider_created_at: Optional[datetime] = Field(default=None, alias="providerCreatedAt")
    provider_updated_at: Optional[datetime] = Field(default=None, alias="providerUpdatedAt")
    iri: Optional[StrictStr] = None
    impersonating_organization: Optional[StrictBool] = Field(default=None, alias="impersonatingOrganization")
    second_auth_factor: Optional[StrictBool] = Field(default=None, alias="secondAuthFactor")
    processor_status: Optional[StrictStr] = Field(default=None, description="Automagically infer on what state the entity is at the Payment Processor.", alias="processorStatus")
    __properties: ClassVar[List[str]] = ["id", "mainAddress", "firstName", "lastName", "publicName", "roleInCompany", "birthday", "email", "roles", "totpEnabled", "intlPhoneNumber", "originCountry", "homeCountry", "preferredLanguage", "lastSuccessfulLogIn", "avatar", "createdAt", "updatedAt", "consentMailAds", "lockdown", "organization", "bankAccount", "identityVerifiedAt", "profiles", "cards", "wallet", "providerName", "providerCreatedAt", "providerUpdatedAt", "iri", "impersonatingOrganization", "secondAuthFactor", "processorStatus"]

    @field_validator('roles')
    def roles_validate_enum(cls, value):
        """Validates the enum"""
        for i in value:
            if i not in set(['ROLE_ORGANIZATION_OWNER', 'ROLE_ADMIN', 'ROLE_CONSULTANT', 'ROLE_ACCOUNTING_MANAGER', 'ROLE_BILLING_MANAGER', 'ROLE_CUSTOMER_SERVICE', 'ROLE_PLATFORM_SUPPORT', 'ROLE_PLATFORM_ADMIN', 'ROLE_USER']):
                raise ValueError("each list item must be one of ('ROLE_ORGANIZATION_OWNER', 'ROLE_ADMIN', 'ROLE_CONSULTANT', 'ROLE_ACCOUNTING_MANAGER', 'ROLE_BILLING_MANAGER', 'ROLE_CUSTOMER_SERVICE', 'ROLE_PLATFORM_SUPPORT', 'ROLE_PLATFORM_ADMIN', 'ROLE_USER')")
        return value

    @field_validator('processor_status')
    def processor_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['unallocated', 'allocating', 'allocated', 'freed', 'outdated']):
            raise ValueError("must be one of enum values ('unallocated', 'allocating', 'allocated', 'freed', 'outdated')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UserAuthenticatedRead from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "created_at",
            "updated_at",
            "provider_created_at",
            "provider_updated_at",
            "iri",
            "impersonating_organization",
            "second_auth_factor",
            "processor_status",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of avatar
        if self.avatar:
            _dict['avatar'] = self.avatar.to_dict()
        # override the default output from pydantic by calling `to_dict()` of organization
        if self.organization:
            _dict['organization'] = self.organization.to_dict()
        # override the default output from pydantic by calling `to_dict()` of bank_account
        if self.bank_account:
            _dict['bankAccount'] = self.bank_account.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in profiles (list)
        _items = []
        if self.profiles:
            for _item_profiles in self.profiles:
                if _item_profiles:
                    _items.append(_item_profiles.to_dict())
            _dict['profiles'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in cards (list)
        _items = []
        if self.cards:
            for _item_cards in self.cards:
                if _item_cards:
                    _items.append(_item_cards.to_dict())
            _dict['cards'] = _items
        # override the default output from pydantic by calling `to_dict()` of wallet
        if self.wallet:
            _dict['wallet'] = self.wallet.to_dict()
        # set to None if public_name (nullable) is None
        # and model_fields_set contains the field
        if self.public_name is None and "public_name" in self.model_fields_set:
            _dict['publicName'] = None

        # set to None if role_in_company (nullable) is None
        # and model_fields_set contains the field
        if self.role_in_company is None and "role_in_company" in self.model_fields_set:
            _dict['roleInCompany'] = None

        # set to None if birthday (nullable) is None
        # and model_fields_set contains the field
        if self.birthday is None and "birthday" in self.model_fields_set:
            _dict['birthday'] = None

        # set to None if intl_phone_number (nullable) is None
        # and model_fields_set contains the field
        if self.intl_phone_number is None and "intl_phone_number" in self.model_fields_set:
            _dict['intlPhoneNumber'] = None

        # set to None if origin_country (nullable) is None
        # and model_fields_set contains the field
        if self.origin_country is None and "origin_country" in self.model_fields_set:
            _dict['originCountry'] = None

        # set to None if home_country (nullable) is None
        # and model_fields_set contains the field
        if self.home_country is None and "home_country" in self.model_fields_set:
            _dict['homeCountry'] = None

        # set to None if preferred_language (nullable) is None
        # and model_fields_set contains the field
        if self.preferred_language is None and "preferred_language" in self.model_fields_set:
            _dict['preferredLanguage'] = None

        # set to None if last_successful_log_in (nullable) is None
        # and model_fields_set contains the field
        if self.last_successful_log_in is None and "last_successful_log_in" in self.model_fields_set:
            _dict['lastSuccessfulLogIn'] = None

        # set to None if avatar (nullable) is None
        # and model_fields_set contains the field
        if self.avatar is None and "avatar" in self.model_fields_set:
            _dict['avatar'] = None

        # set to None if organization (nullable) is None
        # and model_fields_set contains the field
        if self.organization is None and "organization" in self.model_fields_set:
            _dict['organization'] = None

        # set to None if bank_account (nullable) is None
        # and model_fields_set contains the field
        if self.bank_account is None and "bank_account" in self.model_fields_set:
            _dict['bankAccount'] = None

        # set to None if identity_verified_at (nullable) is None
        # and model_fields_set contains the field
        if self.identity_verified_at is None and "identity_verified_at" in self.model_fields_set:
            _dict['identityVerifiedAt'] = None

        # set to None if wallet (nullable) is None
        # and model_fields_set contains the field
        if self.wallet is None and "wallet" in self.model_fields_set:
            _dict['wallet'] = None

        # set to None if provider_name (nullable) is None
        # and model_fields_set contains the field
        if self.provider_name is None and "provider_name" in self.model_fields_set:
            _dict['providerName'] = None

        # set to None if provider_created_at (nullable) is None
        # and model_fields_set contains the field
        if self.provider_created_at is None and "provider_created_at" in self.model_fields_set:
            _dict['providerCreatedAt'] = None

        # set to None if provider_updated_at (nullable) is None
        # and model_fields_set contains the field
        if self.provider_updated_at is None and "provider_updated_at" in self.model_fields_set:
            _dict['providerUpdatedAt'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserAuthenticatedRead from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "mainAddress": obj.get("mainAddress"),
            "firstName": obj.get("firstName"),
            "lastName": obj.get("lastName"),
            "publicName": obj.get("publicName"),
            "roleInCompany": obj.get("roleInCompany"),
            "birthday": obj.get("birthday"),
            "email": obj.get("email"),
            "roles": obj.get("roles"),
            "totpEnabled": obj.get("totpEnabled"),
            "intlPhoneNumber": obj.get("intlPhoneNumber"),
            "originCountry": obj.get("originCountry"),
            "homeCountry": obj.get("homeCountry"),
            "preferredLanguage": obj.get("preferredLanguage"),
            "lastSuccessfulLogIn": obj.get("lastSuccessfulLogIn"),
            "avatar": UserMediaAuthenticatedRead.from_dict(obj["avatar"]) if obj.get("avatar") is not None else None,
            "createdAt": obj.get("createdAt"),
            "updatedAt": obj.get("updatedAt"),
            "consentMailAds": obj.get("consentMailAds"),
            "lockdown": obj.get("lockdown"),
            "organization": UserOrganizationAuthenticatedRead.from_dict(obj["organization"]) if obj.get("organization") is not None else None,
            "bankAccount": UserBankAccountAuthenticatedRead.from_dict(obj["bankAccount"]) if obj.get("bankAccount") is not None else None,
            "identityVerifiedAt": obj.get("identityVerifiedAt"),
            "profiles": [UserPersonaAuthenticatedRead.from_dict(_item) for _item in obj["profiles"]] if obj.get("profiles") is not None else None,
            "cards": [UserCardAuthenticatedRead.from_dict(_item) for _item in obj["cards"]] if obj.get("cards") is not None else None,
            "wallet": UserWalletAuthenticatedRead.from_dict(obj["wallet"]) if obj.get("wallet") is not None else None,
            "providerName": obj.get("providerName"),
            "providerCreatedAt": obj.get("providerCreatedAt"),
            "providerUpdatedAt": obj.get("providerUpdatedAt"),
            "iri": obj.get("iri"),
            "impersonatingOrganization": obj.get("impersonatingOrganization"),
            "secondAuthFactor": obj.get("secondAuthFactor"),
            "processorStatus": obj.get("processorStatus")
        })
        return _obj


