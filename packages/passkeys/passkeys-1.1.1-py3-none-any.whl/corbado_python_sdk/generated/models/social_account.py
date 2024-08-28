# coding: utf-8

"""
    Corbado Backend API

     # Introduction This documentation gives an overview of all Corbado Backend API calls to implement passwordless authentication with Passkeys. 

    The version of the OpenAPI document: 2.0.0
    Contact: support@corbado.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class SocialAccount(BaseModel):
    """
    SocialAccount
    """ # noqa: E501
    social_account_id: StrictStr = Field(alias="socialAccountID")
    provider_type: StrictStr = Field(alias="providerType")
    identifier_value: StrictStr = Field(alias="identifierValue")
    user_id: StrictStr = Field(alias="userID")
    foreign_id: StrictStr = Field(alias="foreignID")
    avatar_url: StrictStr = Field(alias="avatarURL")
    full_name: StrictStr = Field(alias="fullName")
    __properties: ClassVar[List[str]] = ["socialAccountID", "providerType", "identifierValue", "userID", "foreignID", "avatarURL", "fullName"]

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
        """Create an instance of SocialAccount from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SocialAccount from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "socialAccountID": obj.get("socialAccountID"),
            "providerType": obj.get("providerType"),
            "identifierValue": obj.get("identifierValue"),
            "userID": obj.get("userID"),
            "foreignID": obj.get("foreignID"),
            "avatarURL": obj.get("avatarURL"),
            "fullName": obj.get("fullName")
        })
        return _obj


