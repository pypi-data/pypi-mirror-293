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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from ri.apiclient.models.category_summary_metric import CategorySummaryMetric
from ri.apiclient.models.model_perf_metric import ModelPerfMetric
from ri.apiclient.models.result_summary_counts import ResultSummaryCounts
from ri.apiclient.models.risk_score import RiskScore
from ri.apiclient.models.severity_counts import SeverityCounts
from typing import Optional, Set
from typing_extensions import Self

class TestRunMetrics(BaseModel):
    """
    TestRunMetrics returns metrics for a test run.
    """ # noqa: E501
    average_prediction: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The average prediction for the test run (only defined for a subset of tasks such as binary classification).", alias="averagePrediction")
    category_summary_metrics: Optional[List[CategorySummaryMetric]] = Field(default=None, description="The list of category summary metrics.", alias="categorySummaryMetrics")
    duration_millis: Optional[StrictStr] = Field(default=None, description="The duration of the test run in milliseconds.", alias="durationMillis")
    model_perf: Optional[Dict[str, ModelPerfMetric]] = Field(default=None, description="The model performance over the test run as computed using various metrics.", alias="modelPerf")
    num_failing_inputs: Optional[StrictStr] = Field(default=None, description="The number of failing inputs.", alias="numFailingInputs")
    num_inputs: Optional[StrictStr] = Field(default=None, description="The number of inputs. For tabular data, an input is one row.", alias="numInputs")
    risk_scores: Optional[List[RiskScore]] = Field(default=None, description="The list of risk scores.", alias="riskScores")
    severity_counts: Optional[SeverityCounts] = Field(default=None, alias="severityCounts")
    summary_counts: Optional[ResultSummaryCounts] = Field(default=None, alias="summaryCounts")
    __properties: ClassVar[List[str]] = ["averagePrediction", "categorySummaryMetrics", "durationMillis", "modelPerf", "numFailingInputs", "numInputs", "riskScores", "severityCounts", "summaryCounts"]

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
        """Create an instance of TestRunMetrics from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in category_summary_metrics (list)
        _items = []
        if self.category_summary_metrics:
            for _item in self.category_summary_metrics:
                if _item:
                    _items.append(_item.to_dict())
            _dict['categorySummaryMetrics'] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in model_perf (dict)
        _field_dict = {}
        if self.model_perf:
            for _key in self.model_perf:
                if self.model_perf[_key]:
                    _field_dict[_key] = self.model_perf[_key].to_dict()
            _dict['modelPerf'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each item in risk_scores (list)
        _items = []
        if self.risk_scores:
            for _item in self.risk_scores:
                if _item:
                    _items.append(_item.to_dict())
            _dict['riskScores'] = _items
        # override the default output from pydantic by calling `to_dict()` of severity_counts
        if self.severity_counts:
            _dict['severityCounts'] = self.severity_counts.to_dict()
        # override the default output from pydantic by calling `to_dict()` of summary_counts
        if self.summary_counts:
            _dict['summaryCounts'] = self.summary_counts.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestRunMetrics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "averagePrediction": obj.get("averagePrediction"),
            "categorySummaryMetrics": [CategorySummaryMetric.from_dict(_item) for _item in obj["categorySummaryMetrics"]] if obj.get("categorySummaryMetrics") is not None else None,
            "durationMillis": obj.get("durationMillis"),
            "modelPerf": dict(
                (_k, ModelPerfMetric.from_dict(_v))
                for _k, _v in obj["modelPerf"].items()
            )
            if obj.get("modelPerf") is not None
            else None,
            "numFailingInputs": obj.get("numFailingInputs"),
            "numInputs": obj.get("numInputs"),
            "riskScores": [RiskScore.from_dict(_item) for _item in obj["riskScores"]] if obj.get("riskScores") is not None else None,
            "severityCounts": SeverityCounts.from_dict(obj["severityCounts"]) if obj.get("severityCounts") is not None else None,
            "summaryCounts": ResultSummaryCounts.from_dict(obj["summaryCounts"]) if obj.get("summaryCounts") is not None else None
        })
        return _obj


