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


class ModelTask(str, Enum):
    """
    ModelTask
    """

    """
    allowed enum values
    """
    MODEL_TASK_REGRESSION = 'MODEL_TASK_REGRESSION'
    MODEL_TASK_BINARY_CLASSIFICATION = 'MODEL_TASK_BINARY_CLASSIFICATION'
    MODEL_TASK_MULTICLASS_CLASSIFICATION = 'MODEL_TASK_MULTICLASS_CLASSIFICATION'
    MODEL_TASK_NAMED_ENTITY_RECOGNITION = 'MODEL_TASK_NAMED_ENTITY_RECOGNITION'
    MODEL_TASK_RANKING = 'MODEL_TASK_RANKING'
    MODEL_TASK_OBJECT_DETECTION = 'MODEL_TASK_OBJECT_DETECTION'
    MODEL_TASK_NATURAL_LANGUAGE_INFERENCE = 'MODEL_TASK_NATURAL_LANGUAGE_INFERENCE'
    MODEL_TASK_FILL_MASK = 'MODEL_TASK_FILL_MASK'
    MODEL_TASK_ANOMALY_DETECTION = 'MODEL_TASK_ANOMALY_DETECTION'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ModelTask from a JSON string"""
        return cls(json.loads(json_str))


