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
from ri.apiclient.models.id import ID
from ri.apiclient.models.metadata import Metadata
from ri.apiclient.models.pred_info import PredInfo
from ri.apiclient.models.validity_status import ValidityStatus
from typing import Optional, Set
from typing_extensions import Self

class PredictionPrediction(BaseModel):
    """
    Prediction represents a full entry in the Predictions Registry, with info, metadata, and tags used to identify the predictions both internally and to an external user.
    """ # noqa: E501
    creation_time: Optional[datetime] = Field(default=None, alias="creationTime")
    creator_id: Optional[ID] = Field(default=None, alias="creatorId")
    dataset_id: Optional[StrictStr] = Field(default=None, description="The dataset_id and model_id are used to uniquely identify a prediction. These must be provided by the user.", alias="datasetId")
    integration_id: Optional[ID] = Field(default=None, alias="integrationId")
    marked_for_delete_at: Optional[datetime] = Field(default=None, description="If marked_for_delete_at is set, the document will be deleted after a TTL.", alias="markedForDeleteAt")
    model_id: Optional[ID] = Field(default=None, alias="modelId")
    pred_info: Optional[PredInfo] = Field(default=None, alias="predInfo")
    project_ids: Optional[List[ID]] = Field(default=None, description="For now, a pred will only have one project_id associated with it. We make this an array to allow pred's to be shared in the future.", alias="projectIds")
    user_metadata: Optional[Metadata] = Field(default=None, alias="userMetadata")
    validity_status: Optional[ValidityStatus] = Field(default=None, alias="validityStatus")
    validity_status_message: Optional[StrictStr] = Field(default=None, description="Information about the validity status of the predictions, such as why it is invalid. A Case where this would be populated is when the ValidityStatus is not explicitly set to valid by the XP validation task and additional details are required to convey to the user why the predictions are not valid.", alias="validityStatusMessage")
    __properties: ClassVar[List[str]] = ["creationTime", "creatorId", "datasetId", "integrationId", "markedForDeleteAt", "modelId", "predInfo", "projectIds", "userMetadata", "validityStatus", "validityStatusMessage"]

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
        """Create an instance of PredictionPrediction from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of creator_id
        if self.creator_id:
            _dict['creatorId'] = self.creator_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of integration_id
        if self.integration_id:
            _dict['integrationId'] = self.integration_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of model_id
        if self.model_id:
            _dict['modelId'] = self.model_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pred_info
        if self.pred_info:
            _dict['predInfo'] = self.pred_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in project_ids (list)
        _items = []
        if self.project_ids:
            for _item in self.project_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['projectIds'] = _items
        # override the default output from pydantic by calling `to_dict()` of user_metadata
        if self.user_metadata:
            _dict['userMetadata'] = self.user_metadata.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PredictionPrediction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "creationTime": obj.get("creationTime"),
            "creatorId": ID.from_dict(obj["creatorId"]) if obj.get("creatorId") is not None else None,
            "datasetId": obj.get("datasetId"),
            "integrationId": ID.from_dict(obj["integrationId"]) if obj.get("integrationId") is not None else None,
            "markedForDeleteAt": obj.get("markedForDeleteAt"),
            "modelId": ID.from_dict(obj["modelId"]) if obj.get("modelId") is not None else None,
            "predInfo": PredInfo.from_dict(obj["predInfo"]) if obj.get("predInfo") is not None else None,
            "projectIds": [ID.from_dict(_item) for _item in obj["projectIds"]] if obj.get("projectIds") is not None else None,
            "userMetadata": Metadata.from_dict(obj["userMetadata"]) if obj.get("userMetadata") is not None else None,
            "validityStatus": obj.get("validityStatus"),
            "validityStatusMessage": obj.get("validityStatusMessage")
        })
        return _obj


