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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.id import ID
from ri.apiclient.models.model_task import ModelTask
from ri.apiclient.models.profiling_config import ProfilingConfig
from ri.apiclient.models.run_time_info import RunTimeInfo
from typing import Optional, Set
from typing_extensions import Self

class CreateProjectRequest(BaseModel):
    """
    CreateProjectRequest defines a request to create a new Project.
    """ # noqa: E501
    description: StrictStr
    ethical_consideration: Optional[StrictStr] = Field(default=None, alias="ethicalConsideration")
    is_published: Optional[StrictBool] = Field(default=None, description="Published projects are shown on the Workspace overview page.", alias="isPublished")
    model_task: Optional[ModelTask] = Field(default=None, alias="modelTask")
    name: StrictStr
    profiling_config: Optional[ProfilingConfig] = Field(default=None, alias="profilingConfig")
    run_time_info: Optional[RunTimeInfo] = Field(default=None, alias="runTimeInfo")
    tags: Optional[List[StrictStr]] = Field(default=None, description="List of tags associated with the Project to help organizing Projects.")
    use_case: Optional[StrictStr] = Field(default=None, alias="useCase")
    workspace_id: Optional[ID] = Field(default=None, alias="workspaceId")
    __properties: ClassVar[List[str]] = ["description", "ethicalConsideration", "isPublished", "modelTask", "name", "profilingConfig", "runTimeInfo", "tags", "useCase", "workspaceId"]

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
        """Create an instance of CreateProjectRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of profiling_config
        if self.profiling_config:
            _dict['profilingConfig'] = self.profiling_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of run_time_info
        if self.run_time_info:
            _dict['runTimeInfo'] = self.run_time_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of workspace_id
        if self.workspace_id:
            _dict['workspaceId'] = self.workspace_id.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateProjectRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "description": obj.get("description"),
            "ethicalConsideration": obj.get("ethicalConsideration"),
            "isPublished": obj.get("isPublished"),
            "modelTask": obj.get("modelTask"),
            "name": obj.get("name"),
            "profilingConfig": ProfilingConfig.from_dict(obj["profilingConfig"]) if obj.get("profilingConfig") is not None else None,
            "runTimeInfo": RunTimeInfo.from_dict(obj["runTimeInfo"]) if obj.get("runTimeInfo") is not None else None,
            "tags": obj.get("tags"),
            "useCase": obj.get("useCase"),
            "workspaceId": ID.from_dict(obj["workspaceId"]) if obj.get("workspaceId") is not None else None
        })
        return _obj


