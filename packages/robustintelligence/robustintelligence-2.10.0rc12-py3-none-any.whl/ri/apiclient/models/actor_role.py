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


class ActorRole(str, Enum):
    """
    ActorRole specifies a set of permissions an actor has on an object.   - ACTOR_ROLE_ADMIN: Admin role has full manage access to the object, including deletion and adding users.  - ACTOR_ROLE_USER: User role has edit and view access to the object.  - ACTOR_ROLE_SUPPORT: Support role is used by RI support engineers.  - ACTOR_ROLE_VIEWER: Viewer role is read-only.  - ACTOR_ROLE_NONE: None role has no permissions to the object.  - ACTOR_ROLE_VP: VP role has full manage access to the object, including deletion and adding users.
    """

    """
    allowed enum values
    """
    ACTOR_ROLE_ADMIN = 'ACTOR_ROLE_ADMIN'
    ACTOR_ROLE_USER = 'ACTOR_ROLE_USER'
    ACTOR_ROLE_SUPPORT = 'ACTOR_ROLE_SUPPORT'
    ACTOR_ROLE_VIEWER = 'ACTOR_ROLE_VIEWER'
    ACTOR_ROLE_NONE = 'ACTOR_ROLE_NONE'
    ACTOR_ROLE_VP = 'ACTOR_ROLE_VP'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ActorRole from a JSON string"""
        return cls(json.loads(json_str))


