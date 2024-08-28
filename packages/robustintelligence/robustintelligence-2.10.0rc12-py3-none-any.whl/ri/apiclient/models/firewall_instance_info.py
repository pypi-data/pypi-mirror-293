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
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.firewall_instance_deployment_config import FirewallInstanceDeploymentConfig
from ri.apiclient.models.firewall_instance_status import FirewallInstanceStatus
from ri.apiclient.models.firewall_rule_config import FirewallRuleConfig
from ri.apiclient.models.id import ID
from typing import Optional, Set
from typing_extensions import Self

class FirewallInstanceInfo(BaseModel):
    """
    Information about a single Firewall Instance, including its configuration and the current status of its deployment.
    """ # noqa: E501
    agent_id: Optional[ID] = Field(default=None, alias="agentId")
    config: Optional[FirewallRuleConfig] = None
    deployment_status: Optional[FirewallInstanceStatus] = Field(default=None, alias="deploymentStatus")
    description: Optional[StrictStr] = Field(default=None, description="Optional human-readable description of the firewall instance.")
    firewall_instance_id: Optional[ID] = Field(default=None, alias="firewallInstanceId")
    last_heartbeat_time: Optional[datetime] = Field(default=None, description="Last time the control plan received a heartbeat from the firewall instance.", alias="lastHeartbeatTime")
    spec: Optional[FirewallInstanceDeploymentConfig] = None
    __properties: ClassVar[List[str]] = ["agentId", "config", "deploymentStatus", "description", "firewallInstanceId", "lastHeartbeatTime", "spec"]

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
        """Create an instance of FirewallInstanceInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of agent_id
        if self.agent_id:
            _dict['agentId'] = self.agent_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of config
        if self.config:
            _dict['config'] = self.config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of firewall_instance_id
        if self.firewall_instance_id:
            _dict['firewallInstanceId'] = self.firewall_instance_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of spec
        if self.spec:
            _dict['spec'] = self.spec.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of FirewallInstanceInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "agentId": ID.from_dict(obj["agentId"]) if obj.get("agentId") is not None else None,
            "config": FirewallRuleConfig.from_dict(obj["config"]) if obj.get("config") is not None else None,
            "deploymentStatus": obj.get("deploymentStatus"),
            "description": obj.get("description"),
            "firewallInstanceId": ID.from_dict(obj["firewallInstanceId"]) if obj.get("firewallInstanceId") is not None else None,
            "lastHeartbeatTime": obj.get("lastHeartbeatTime"),
            "spec": FirewallInstanceDeploymentConfig.from_dict(obj["spec"]) if obj.get("spec") is not None else None
        })
        return _obj


