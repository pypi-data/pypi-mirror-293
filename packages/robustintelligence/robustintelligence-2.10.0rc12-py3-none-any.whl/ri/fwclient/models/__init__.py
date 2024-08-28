# coding: utf-8

# flake8: noqa
"""
    Robust Intelligence Firewall REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Auth-Token` header. Your AI Firewall Agent domain forms the base of the URL for REST API calls. To find the Agent domain in the Robust Intelligence UI, click AI Firewall: Settings icon: Firewall Settings. Find your agent in the Firewall Agent Status: Agents Setup page, and copy its URL from the table.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

# import models into model package
from ri.fwclient.models.any import Any
from ri.fwclient.models.attack_objective import AttackObjective
from ri.fwclient.models.attack_technique import AttackTechnique
from ri.fwclient.models.code_detection_details import CodeDetectionDetails
from ri.fwclient.models.code_detection_rule_config import CodeDetectionRuleConfig
from ri.fwclient.models.code_substring import CodeSubstring
from ri.fwclient.models.create_firewall_instance_request import CreateFirewallInstanceRequest
from ri.fwclient.models.create_firewall_instance_response import CreateFirewallInstanceResponse
from ri.fwclient.models.custom_pii_entity import CustomPiiEntity
from ri.fwclient.models.firewall_action import FirewallAction
from ri.fwclient.models.firewall_instance_deployment_config import FirewallInstanceDeploymentConfig
from ri.fwclient.models.firewall_instance_info import FirewallInstanceInfo
from ri.fwclient.models.firewall_instance_status import FirewallInstanceStatus
from ri.fwclient.models.firewall_rule_config import FirewallRuleConfig
from ri.fwclient.models.firewall_rule_type import FirewallRuleType
from ri.fwclient.models.firewall_tokenizer import FirewallTokenizer
from ri.fwclient.models.flagged_entity import FlaggedEntity
from ri.fwclient.models.flagged_substring import FlaggedSubstring
from ri.fwclient.models.get_firewall_effective_config_response import GetFirewallEffectiveConfigResponse
from ri.fwclient.models.get_firewall_instance_response import GetFirewallInstanceResponse
from ri.fwclient.models.id import ID
from ri.fwclient.models.individual_rules_config import IndividualRulesConfig
from ri.fwclient.models.language import Language
from ri.fwclient.models.language_detection_details import LanguageDetectionDetails
from ri.fwclient.models.language_detection_rule_config import LanguageDetectionRuleConfig
from ri.fwclient.models.language_substring import LanguageSubstring
from ri.fwclient.models.list_firewall_instances_response import ListFirewallInstancesResponse
from ri.fwclient.models.model_info import ModelInfo
from ri.fwclient.models.off_topic_rule_config import OffTopicRuleConfig
from ri.fwclient.models.pii_detection_details import PiiDetectionDetails
from ri.fwclient.models.pii_detection_rule_config import PiiDetectionRuleConfig
from ri.fwclient.models.pii_entity_type import PiiEntityType
from ri.fwclient.models.processed_request import ProcessedRequest
from ri.fwclient.models.product_metadata import ProductMetadata
from ri.fwclient.models.prompt_injection_details import PromptInjectionDetails
from ri.fwclient.models.prompt_injection_rule_config import PromptInjectionRuleConfig
from ri.fwclient.models.raw_model_prediction import RawModelPrediction
from ri.fwclient.models.request_body_component import RequestBodyComponent
from ri.fwclient.models.risk_category_type import RiskCategoryType
from ri.fwclient.models.rpc_status import RpcStatus
from ri.fwclient.models.rule_evaluation_metadata import RuleEvaluationMetadata
from ri.fwclient.models.rule_output import RuleOutput
from ri.fwclient.models.rule_sensitivity import RuleSensitivity
from ri.fwclient.models.standard_info import StandardInfo
from ri.fwclient.models.text_classification_pred import TextClassificationPred
from ri.fwclient.models.token_counter_rule_config import TokenCounterRuleConfig
from ri.fwclient.models.toxicity_detection_details import ToxicityDetectionDetails
from ri.fwclient.models.toxicity_rule_config import ToxicityRuleConfig
from ri.fwclient.models.toxicity_rule_mode import ToxicityRuleMode
from ri.fwclient.models.toxicity_threat_category import ToxicityThreatCategory
from ri.fwclient.models.unknown_external_source_rule_config import UnknownExternalSourceRuleConfig
from ri.fwclient.models.update_firewall_instance_response import UpdateFirewallInstanceResponse
from ri.fwclient.models.update_instance_request import UpdateInstanceRequest
from ri.fwclient.models.validate_request import ValidateRequest
from ri.fwclient.models.validate_response import ValidateResponse
from ri.fwclient.models.yara_info import YaraInfo
