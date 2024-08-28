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
from typing import Any, ClassVar, Dict, List, Optional
from corbado_python_sdk.generated.models.challenge_type import ChallengeType
from corbado_python_sdk.generated.models.client_information import ClientInformation
from typing import Optional, Set
from typing_extensions import Self

class ChallengeCreateReq(BaseModel):
    """
    ChallengeCreateReq
    """ # noqa: E501
    challenge_type: ChallengeType = Field(alias="challengeType")
    identifier_value: StrictStr = Field(alias="identifierValue")
    challenge_metadata: Optional[Dict[str, Any]] = Field(default=None, alias="challengeMetadata")
    client_information: ClientInformation = Field(alias="clientInformation")
    __properties: ClassVar[List[str]] = ["challengeType", "identifierValue", "challengeMetadata", "clientInformation"]

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
        """Create an instance of ChallengeCreateReq from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of client_information
        if self.client_information:
            _dict['clientInformation'] = self.client_information.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ChallengeCreateReq from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "challengeType": obj.get("challengeType"),
            "identifierValue": obj.get("identifierValue"),
            "challengeMetadata": obj.get("challengeMetadata"),
            "clientInformation": ClientInformation.from_dict(obj["clientInformation"]) if obj.get("clientInformation") is not None else None
        })
        return _obj


