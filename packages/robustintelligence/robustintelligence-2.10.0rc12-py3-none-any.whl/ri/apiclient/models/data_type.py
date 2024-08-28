# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class DataType(str, Enum):
    """
    DataType
    """

    """
    allowed enum values
    """
    DATA_TYPE_UNSPECIFIED = 'DATA_TYPE_UNSPECIFIED'
    DATA_TYPE_DELTA_TABLE = 'DATA_TYPE_DELTA_TABLE'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of DataType from a JSON string"""
        return cls(json.loads(json_str))


