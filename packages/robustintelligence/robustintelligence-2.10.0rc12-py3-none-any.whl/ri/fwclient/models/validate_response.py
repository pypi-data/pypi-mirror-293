# coding: utf-8

"""
    Robust Intelligence Firewall REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Auth-Token` header. Your AI Firewall Agent domain forms the base of the URL for REST API calls. To find the Agent domain in the Robust Intelligence UI, click AI Firewall: Settings icon: Firewall Settings. Find your agent in the Firewall Agent Status: Agents Setup page, and copy its URL from the table.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from ri.fwclient.models.processed_request import ProcessedRequest
from ri.fwclient.models.product_metadata import ProductMetadata
from ri.fwclient.models.rule_output import RuleOutput
from typing import Optional, Set
from typing_extensions import Self

class ValidateResponse(BaseModel):
    """
    ValidateResponse is the response to a single validation request. Note: this does not follow the same RI API standards, because we want this to be easily consumed by security team's event frameworks.
    """ # noqa: E501
    api_schema_version: Optional[StrictStr] = Field(default=None, description="API schema version is the version of the API response. This should be updated whenever we make semantic changes to the response.", alias="apiSchemaVersion")
    input_results: Optional[Dict[str, RuleOutput]] = Field(default=None, description="Results of the firewall for user input. The key is a rule name.", alias="inputResults")
    metadata: Optional[ProductMetadata] = None
    output_results: Optional[Dict[str, RuleOutput]] = Field(default=None, description="Results of the firewall for model output. The key is a rule name.", alias="outputResults")
    processed_req: Optional[ProcessedRequest] = Field(default=None, alias="processedReq")
    __properties: ClassVar[List[str]] = ["apiSchemaVersion", "inputResults", "metadata", "outputResults", "processedReq"]

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
        """Create an instance of ValidateResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in input_results (dict)
        _field_dict = {}
        if self.input_results:
            for _key in self.input_results:
                if self.input_results[_key]:
                    _field_dict[_key] = self.input_results[_key].to_dict()
            _dict['inputResults'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in output_results (dict)
        _field_dict = {}
        if self.output_results:
            for _key in self.output_results:
                if self.output_results[_key]:
                    _field_dict[_key] = self.output_results[_key].to_dict()
            _dict['outputResults'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of processed_req
        if self.processed_req:
            _dict['processedReq'] = self.processed_req.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ValidateResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "apiSchemaVersion": obj.get("apiSchemaVersion"),
            "inputResults": dict(
                (_k, RuleOutput.from_dict(_v))
                for _k, _v in obj["inputResults"].items()
            )
            if obj.get("inputResults") is not None
            else None,
            "metadata": ProductMetadata.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None,
            "outputResults": dict(
                (_k, RuleOutput.from_dict(_v))
                for _k, _v in obj["outputResults"].items()
            )
            if obj.get("outputResults") is not None
            else None,
            "processedReq": ProcessedRequest.from_dict(obj["processedReq"]) if obj.get("processedReq") is not None else None
        })
        return _obj


