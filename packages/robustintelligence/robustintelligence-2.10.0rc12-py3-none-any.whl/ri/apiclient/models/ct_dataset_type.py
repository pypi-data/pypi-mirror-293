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


class CTDatasetType(str, Enum):
    """
    CTDatasetType specifies if the registered dataset is user specified or a scheduled ct dataset. TODO(RIME-15612): Attempt to fix these prefixes.   - CTDATASET_TYPE_UNSPECIFIED: protolint:disable:next ENUM_FIELD_NAMES_PREFIX  - CTDATASET_TYPE_USER_SPECIFIED: protolint:disable:next ENUM_FIELD_NAMES_PREFIX  - CTDATASET_TYPE_SCHEDULED_CT: protolint:disable:next ENUM_FIELD_NAMES_PREFIX
    """

    """
    allowed enum values
    """
    CTDATASET_TYPE_UNSPECIFIED = 'CTDATASET_TYPE_UNSPECIFIED'
    CTDATASET_TYPE_USER_SPECIFIED = 'CTDATASET_TYPE_USER_SPECIFIED'
    CTDATASET_TYPE_SCHEDULED_CT = 'CTDATASET_TYPE_SCHEDULED_CT'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of CTDatasetType from a JSON string"""
        return cls(json.loads(json_str))


