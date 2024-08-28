# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.

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

from pydantic import Field, StrictStr, field_validator
from typing import Any, Dict, Optional
from typing_extensions import Annotated
from ri.apiclient.models.create_customer_managed_key_request import CreateCustomerManagedKeyRequest
from ri.apiclient.models.create_customer_managed_key_response import CreateCustomerManagedKeyResponse
from ri.apiclient.models.get_customer_managed_key_response import GetCustomerManagedKeyResponse
from ri.apiclient.models.get_key_status_response import GetKeyStatusResponse

from ri.apiclient.models import *
from ri.apiclient.api_client import ApiClient, RequestSerialized
from ri.apiclient.api_response import ApiResponse
from ri.apiclient.rest import RESTResponseType


class CustomerManagedKeyServiceApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_call
    def create_customer_managed_key(
        self,
        cmk_config: Optional[CustomerManagedKeyConfig] = None,
    ) -> CreateCustomerManagedKeyResponse:
        """CreateCustomerManagedKey

        Creates a new customer managed key. At most one key can exist per deployment.

        :param cmk_config:
        :type cmk_config: CustomerManagedKeyConfig
        :return: Returns the result object.
        """ # noqa: E501

        body = CreateCustomerManagedKeyRequest(
          cmk_config=cmk_config,
        )

        _param = self._create_customer_managed_key_serialize(
            body=body,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CreateCustomerManagedKeyResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    def _create_customer_managed_key_serialize(
        self,
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
            'rime-api-key'
        ]

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v1-beta/customer-managed-key',
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
    def delete_customer_managed_key(
        self,
        cmk_config_kms_key_arn: str,
        cmk_config_key_provider: Optional[str] = None,
    ) -> object:
        """DeleteCustomerManagedKey

        Delete the customer managed key.

        :param cmk_config_kms_key_arn: The ARN of the AWS KMS key to use as the customer managed key. (required)
        :type cmk_config_kms_key_arn: str
        :param cmk_config_key_provider:  - KEY_PROVIDER_AWS_KMS: AWS Key Management Service
        :type cmk_config_key_provider: str
        :return: Returns the result object.
        """ # noqa: E501


        _param = self._delete_customer_managed_key_serialize(
            cmk_config_kms_key_arn=cmk_config_kms_key_arn,
            cmk_config_key_provider=cmk_config_key_provider,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "object",
        }
        response_data = self.api_client.call_api(
            *_param,
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    def _delete_customer_managed_key_serialize(
        self,
        cmk_config_kms_key_arn,
        cmk_config_key_provider,
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

        if cmk_config_key_provider is not None:
            
            _query_params.append(('cmkConfig.keyProvider', cmk_config_key_provider))
            
        if cmk_config_kms_key_arn is not None:
            
            _query_params.append(('cmkConfig.kmsKeyArn', cmk_config_kms_key_arn))
            
        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'application/json'
            ]
        )


        _auth_settings: List[str] = [
            'rime-api-key'
        ]

        return self.api_client.param_serialize(
            method='DELETE',
            resource_path='/v1-beta/customer-managed-key',
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
    def get_customer_managed_key(
        self,
        cmk_config_kms_key_arn: str,
        cmk_config_key_provider: Optional[str] = None,
    ) -> GetCustomerManagedKeyResponse:
        """GetCustomerManagedKey

        Returns a customer managed key if one has been created.

        :param cmk_config_kms_key_arn: The ARN of the AWS KMS key to use as the customer managed key. (required)
        :type cmk_config_kms_key_arn: str
        :param cmk_config_key_provider:  - KEY_PROVIDER_AWS_KMS: AWS Key Management Service
        :type cmk_config_key_provider: str
        :return: Returns the result object.
        """ # noqa: E501


        _param = self._get_customer_managed_key_serialize(
            cmk_config_kms_key_arn=cmk_config_kms_key_arn,
            cmk_config_key_provider=cmk_config_key_provider,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetCustomerManagedKeyResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    def _get_customer_managed_key_serialize(
        self,
        cmk_config_kms_key_arn,
        cmk_config_key_provider,
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

        if cmk_config_key_provider is not None:
            
            _query_params.append(('cmkConfig.keyProvider', cmk_config_key_provider))
            
        if cmk_config_kms_key_arn is not None:
            
            _query_params.append(('cmkConfig.kmsKeyArn', cmk_config_kms_key_arn))
            
        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'application/json'
            ]
        )


        _auth_settings: List[str] = [
            'rime-api-key'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1-beta/customer-managed-key',
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
    def get_key_status(
        self,
    ) -> GetKeyStatusResponse:
        """GetKeyStatus

        Return whether the customer managed key is active or revoked.

        :return: Returns the result object.
        """ # noqa: E501


        _param = self._get_key_status_serialize(
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetKeyStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    def _get_key_status_serialize(
        self,
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

        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'application/json'
            ]
        )


        _auth_settings: List[str] = [
            'rime-api-key'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1-beta/customer-managed-key/status',
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
