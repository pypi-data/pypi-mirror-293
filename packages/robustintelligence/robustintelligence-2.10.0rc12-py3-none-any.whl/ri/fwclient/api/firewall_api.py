# coding: utf-8

"""
    Robust Intelligence Firewall REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Auth-Token` header. Your AI Firewall Agent domain forms the base of the URL for REST API calls. To find the Agent domain in the Robust Intelligence UI, click AI Firewall: Settings icon: Firewall Settings. Find your agent in the Firewall Agent Status: Agents Setup page, and copy its URL from the table.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501
import warnings
from datetime import datetime
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import Field, StrictStr
from typing_extensions import Annotated
from ri.fwclient.models.get_firewall_effective_config_response import GetFirewallEffectiveConfigResponse
from ri.fwclient.models.validate_request import ValidateRequest
from ri.fwclient.models.validate_response import ValidateResponse

from ri.fwclient.models import *
from ri.fwclient.api_client import ApiClient, RequestSerialized
from ri.fwclient.api_response import ApiResponse
from ri.fwclient.rest import RESTResponseType


class FirewallApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_call
    def effective_config(
        self,
        firewall_instance_id_uuid: str,
    ) -> GetFirewallEffectiveConfigResponse:
        """GetFirewallEffectiveConfig

        Retrieve the effective config of the firewall. The effective config is the users config plus all defaults. This request will be routed to a specific FirewallInstance. There can be multiple FirewallInstances in the cluster with different configurations.

        :param firewall_instance_id_uuid: Unique object ID. (required)
        :type firewall_instance_id_uuid: str
        :return: Returns the result object.
        """ # noqa: E501


        _param = self._effective_config_serialize(
            firewall_instance_id_uuid=firewall_instance_id_uuid,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetFirewallEffectiveConfigResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    def _effective_config_serialize(
        self,
        firewall_instance_id_uuid,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        if firewall_instance_id_uuid is not None:
            _path_params['firewallInstanceId.uuid'] = firewall_instance_id_uuid
        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'application/json'
            ]
        )


        _auth_settings: List[str] = [
            'X-Firewall-Auth-Token'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1-beta/firewall/{firewallInstanceId.uuid}/effective-config',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
        )

    @validate_call
    def validate(
        self,
        firewall_instance_id_uuid: str,
        contexts: Optional[List[str]] = None,
        firewall_instance_id: Optional[object] = None,
        output_text: Optional[str] = None,
        user_input_text: Optional[str] = None,
    ) -> ValidateResponse:
        """Validate

        Validate performs real-time validation on a single query to the model. This request will be routed to a specific FirewallInstance. There can be multiple FirewallInstances in the cluster with different configurations.

        :param firewall_instance_id_uuid: Unique object ID. (required)
        :type firewall_instance_id_uuid: str
        :param contexts: Documents that represent relevant context for the input query that is fed into the model. e.g. in a RAG application this will be the documents loaded during the RAG Retrieval phase to augment the LLM's response.
        :type contexts: List[str]
        :param firewall_instance_id: Unique ID of an object in RIME.
        :type firewall_instance_id: object
        :param output_text: Output text is the raw output text of the model. The generative firewall performs validation on the output so the system can determine whether to show it to users.
        :type output_text: str
        :param user_input_text: Input text is the raw user input. The generative firewall performs validation on input to prevent risk configured by firewall rules.
        :type user_input_text: str
        :return: Returns the result object.
        """ # noqa: E501

        body = ValidateRequest(
          contexts=contexts,
          firewall_instance_id=firewall_instance_id,
          output_text=output_text,
          user_input_text=user_input_text,
        )

        _param = self._validate_serialize(
            firewall_instance_id_uuid=firewall_instance_id_uuid,
            body=body,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ValidateResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    def _validate_serialize(
        self,
        firewall_instance_id_uuid,
        body,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        if firewall_instance_id_uuid is not None:
            _path_params['firewallInstanceId.uuid'] = firewall_instance_id_uuid
        if body is not None:
            _body_params = body
        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'application/json'
            ]
        )

        _default_content_type = (
            self.api_client.select_header_content_type(
                [
                    'application/json'
                ]
            )
        )
        if _default_content_type is not None:
            _header_params['Content-Type'] = _default_content_type

        _auth_settings: List[str] = [
            'X-Firewall-Auth-Token'
        ]

        return self.api_client.param_serialize(
            method='PUT',
            resource_path='/v1-beta/firewall/{firewallInstanceId.uuid}/validate',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
        )
