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


class FilescanningPackageType(str, Enum):
    """
    The package type or protocol.
    """

    """
    allowed enum values
    """
    PACKAGE_TYPE_UNSPECIFIED = 'PACKAGE_TYPE_UNSPECIFIED'
    PACKAGE_TYPE_HUGGINGFACE = 'PACKAGE_TYPE_HUGGINGFACE'
    PACKAGE_TYPE_MLFLOW = 'PACKAGE_TYPE_MLFLOW'
    PACKAGE_TYPE_MAVEN = 'PACKAGE_TYPE_MAVEN'
    PACKAGE_TYPE_NPM = 'PACKAGE_TYPE_NPM'
    PACKAGE_TYPE_NUGET = 'PACKAGE_TYPE_NUGET'
    PACKAGE_TYPE_GEM = 'PACKAGE_TYPE_GEM'
    PACKAGE_TYPE_PYPI = 'PACKAGE_TYPE_PYPI'
    PACKAGE_TYPE_GITHUB = 'PACKAGE_TYPE_GITHUB'
    PACKAGE_TYPE_BITBUCKET = 'PACKAGE_TYPE_BITBUCKET'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of FilescanningPackageType from a JSON string"""
        return cls(json.loads(json_str))


