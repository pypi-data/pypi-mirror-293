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
from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from tpdk_safe_checkout.models.card_metadata_read import CardMetadataRead
from typing import Optional, Set
from typing_extensions import Self

class CardRead(BaseModel):
    """
    
    """ # noqa: E501
    primary_account_number: Optional[StrictStr] = Field(default=None, alias="primaryAccountNumber")
    expire_at: datetime = Field(alias="expireAt")
    currency: Optional[StrictStr] = None
    country_code: Optional[StrictStr] = Field(default=None, alias="countryCode")
    brand: Optional[StrictStr] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    metadata: Optional[List[CardMetadataRead]] = None
    provider_name: Optional[StrictStr] = Field(default=None, alias="providerName")
    provider_created_at: Optional[datetime] = Field(default=None, alias="providerCreatedAt")
    provider_updated_at: Optional[datetime] = Field(default=None, alias="providerUpdatedAt")
    iri: Optional[StrictStr] = None
    processor_status: Optional[StrictStr] = Field(default=None, description="Automagically infer on what state the entity is at the Payment Processor.", alias="processorStatus")
    __properties: ClassVar[List[str]] = ["primaryAccountNumber", "expireAt", "currency", "countryCode", "brand", "createdAt", "updatedAt", "metadata", "providerName", "providerCreatedAt", "providerUpdatedAt", "iri", "processorStatus"]

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
        """Create an instance of CardRead from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "provider_created_at",
            "provider_updated_at",
            "iri",
            "processor_status",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in metadata (list)
        _items = []
        if self.metadata:
            for _item_metadata in self.metadata:
                if _item_metadata:
                    _items.append(_item_metadata.to_dict())
            _dict['metadata'] = _items
        # set to None if primary_account_number (nullable) is None
        # and model_fields_set contains the field
        if self.primary_account_number is None and "primary_account_number" in self.model_fields_set:
            _dict['primaryAccountNumber'] = None

        # set to None if currency (nullable) is None
        # and model_fields_set contains the field
        if self.currency is None and "currency" in self.model_fields_set:
            _dict['currency'] = None

        # set to None if country_code (nullable) is None
        # and model_fields_set contains the field
        if self.country_code is None and "country_code" in self.model_fields_set:
            _dict['countryCode'] = None

        # set to None if brand (nullable) is None
        # and model_fields_set contains the field
        if self.brand is None and "brand" in self.model_fields_set:
            _dict['brand'] = None

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
        """Create an instance of CardRead from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "primaryAccountNumber": obj.get("primaryAccountNumber"),
            "expireAt": obj.get("expireAt"),
            "currency": obj.get("currency"),
            "countryCode": obj.get("countryCode"),
            "brand": obj.get("brand"),
            "createdAt": obj.get("createdAt"),
            "updatedAt": obj.get("updatedAt"),
            "metadata": [CardMetadataRead.from_dict(_item) for _item in obj["metadata"]] if obj.get("metadata") is not None else None,
            "providerName": obj.get("providerName"),
            "providerCreatedAt": obj.get("providerCreatedAt"),
            "providerUpdatedAt": obj.get("providerUpdatedAt"),
            "iri": obj.get("iri"),
            "processorStatus": obj.get("processorStatus")
        })
        return _obj


