# coding: utf-8

"""
    Safe Checkout

    Simple, yet elegant web interfaces for your convenience. One request away from your first secured C2C transaction.

    The version of the OpenAPI document: 2.0.23
    Contact: noc@tripartie.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class QuoteWrite(BaseModel):
    """
    Someone has to ask for a Quote prior to create a transaction and (therefor) charging a known amount of money.
    """ # noqa: E501
    captcha: Optional[StrictStr] = None
    offer: Optional[StrictStr] = None
    shipping_carrier: StrictStr = Field(alias="shippingCarrier")
    quantity_to_be_acquired: StrictInt = Field(alias="quantityToBeAcquired")
    attempt_unit_price: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="attemptUnitPrice")
    __properties: ClassVar[List[str]] = ["captcha", "offer", "shippingCarrier", "quantityToBeAcquired", "attemptUnitPrice"]

    @field_validator('shipping_carrier')
    def shipping_carrier_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['SwissPost', 'Colissimo', 'MondialRelay']):
            raise ValueError("must be one of enum values ('SwissPost', 'Colissimo', 'MondialRelay')")
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
        """Create an instance of QuoteWrite from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if captcha (nullable) is None
        # and model_fields_set contains the field
        if self.captcha is None and "captcha" in self.model_fields_set:
            _dict['captcha'] = None

        # set to None if offer (nullable) is None
        # and model_fields_set contains the field
        if self.offer is None and "offer" in self.model_fields_set:
            _dict['offer'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of QuoteWrite from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "captcha": obj.get("captcha"),
            "offer": obj.get("offer"),
            "shippingCarrier": obj.get("shippingCarrier"),
            "quantityToBeAcquired": obj.get("quantityToBeAcquired") if obj.get("quantityToBeAcquired") is not None else 1,
            "attemptUnitPrice": obj.get("attemptUnitPrice")
        })
        return _obj


