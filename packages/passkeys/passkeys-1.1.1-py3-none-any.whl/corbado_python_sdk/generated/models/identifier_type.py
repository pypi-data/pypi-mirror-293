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
import json
from enum import Enum
from typing_extensions import Self


class IdentifierType(str, Enum):
    """
    IdentifierType
    """

    """
    allowed enum values
    """
    EMAIL = 'email'
    PHONE = 'phone'
    USERNAME = 'username'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of IdentifierType from a JSON string"""
        return cls(json.loads(json_str))


