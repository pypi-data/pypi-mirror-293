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


class ObjectiveSubCategory(str, Enum):
    """
    ObjectiveSubCategory is the specific intent that the attack prompt is trying to achieve.
    """

    """
    allowed enum values
    """
    OBJECTIVE_SUB_CATEGORY_THEFT = 'OBJECTIVE_SUB_CATEGORY_THEFT'
    OBJECTIVE_SUB_CATEGORY_POISONING = 'OBJECTIVE_SUB_CATEGORY_POISONING'
    OBJECTIVE_SUB_CATEGORY_STALKING = 'OBJECTIVE_SUB_CATEGORY_STALKING'
    OBJECTIVE_SUB_CATEGORY_TERRORISM = 'OBJECTIVE_SUB_CATEGORY_TERRORISM'
    OBJECTIVE_SUB_CATEGORY_BOMB = 'OBJECTIVE_SUB_CATEGORY_BOMB'
    OBJECTIVE_SUB_CATEGORY_MURDER = 'OBJECTIVE_SUB_CATEGORY_MURDER'
    OBJECTIVE_SUB_CATEGORY_PIRACY = 'OBJECTIVE_SUB_CATEGORY_PIRACY'
    OBJECTIVE_SUB_CATEGORY_VIRUS = 'OBJECTIVE_SUB_CATEGORY_VIRUS'
    OBJECTIVE_SUB_CATEGORY_MISINFORMATION = 'OBJECTIVE_SUB_CATEGORY_MISINFORMATION'
    OBJECTIVE_SUB_CATEGORY_FINANCIAL_ADVICE = 'OBJECTIVE_SUB_CATEGORY_FINANCIAL_ADVICE'
    OBJECTIVE_SUB_CATEGORY_PII = 'OBJECTIVE_SUB_CATEGORY_PII'
    OBJECTIVE_SUB_CATEGORY_PROMPT_EXTRACTION = 'OBJECTIVE_SUB_CATEGORY_PROMPT_EXTRACTION'
    OBJECTIVE_SUB_CATEGORY_COPYRIGHT_EXTRACTION = 'OBJECTIVE_SUB_CATEGORY_COPYRIGHT_EXTRACTION'
    OBJECTIVE_SUB_CATEGORY_DRUGS = 'OBJECTIVE_SUB_CATEGORY_DRUGS'
    OBJECTIVE_SUB_CATEGORY_SUICIDE = 'OBJECTIVE_SUB_CATEGORY_SUICIDE'
    OBJECTIVE_SUB_CATEGORY_ANIMAL_VIOLENCE = 'OBJECTIVE_SUB_CATEGORY_ANIMAL_VIOLENCE'
    OBJECTIVE_SUB_CATEGORY_BRANDED_CONTENT = 'OBJECTIVE_SUB_CATEGORY_BRANDED_CONTENT'
    OBJECTIVE_SUB_CATEGORY_BULLYING = 'OBJECTIVE_SUB_CATEGORY_BULLYING'
    OBJECTIVE_SUB_CATEGORY_CELEBRITY_PII = 'OBJECTIVE_SUB_CATEGORY_CELEBRITY_PII'
    OBJECTIVE_SUB_CATEGORY_CHEATING = 'OBJECTIVE_SUB_CATEGORY_CHEATING'
    OBJECTIVE_SUB_CATEGORY_CHILD_SEXUAL_ABUSE_MATERIAL = 'OBJECTIVE_SUB_CATEGORY_CHILD_SEXUAL_ABUSE_MATERIAL'
    OBJECTIVE_SUB_CATEGORY_DISABILITIES = 'OBJECTIVE_SUB_CATEGORY_DISABILITIES'
    OBJECTIVE_SUB_CATEGORY_ECONOMIC_CLASS = 'OBJECTIVE_SUB_CATEGORY_ECONOMIC_CLASS'
    OBJECTIVE_SUB_CATEGORY_EMOTIONAL_ABUSE = 'OBJECTIVE_SUB_CATEGORY_EMOTIONAL_ABUSE'
    OBJECTIVE_SUB_CATEGORY_FIREARMS = 'OBJECTIVE_SUB_CATEGORY_FIREARMS'
    OBJECTIVE_SUB_CATEGORY_HUMAN_EXPLOITATION = 'OBJECTIVE_SUB_CATEGORY_HUMAN_EXPLOITATION'
    OBJECTIVE_SUB_CATEGORY_IMMIGRATION_STATUS = 'OBJECTIVE_SUB_CATEGORY_IMMIGRATION_STATUS'
    OBJECTIVE_SUB_CATEGORY_IMPERSONATION_IMPOSTOR_CONTENT = 'OBJECTIVE_SUB_CATEGORY_IMPERSONATION_IMPOSTOR_CONTENT'
    OBJECTIVE_SUB_CATEGORY_INTELLECTUAL_PROPERTY_PIRACY = 'OBJECTIVE_SUB_CATEGORY_INTELLECTUAL_PROPERTY_PIRACY'
    OBJECTIVE_SUB_CATEGORY_LOGOS = 'OBJECTIVE_SUB_CATEGORY_LOGOS'
    OBJECTIVE_SUB_CATEGORY_MARITAL_STATUS = 'OBJECTIVE_SUB_CATEGORY_MARITAL_STATUS'
    OBJECTIVE_SUB_CATEGORY_MOVIE_QUOTES = 'OBJECTIVE_SUB_CATEGORY_MOVIE_QUOTES'
    OBJECTIVE_SUB_CATEGORY_PERSONAL_IDENTIFICATION_NUMBERS = 'OBJECTIVE_SUB_CATEGORY_PERSONAL_IDENTIFICATION_NUMBERS'
    OBJECTIVE_SUB_CATEGORY_PHISHING = 'OBJECTIVE_SUB_CATEGORY_PHISHING'
    OBJECTIVE_SUB_CATEGORY_PLAGIARISM = 'OBJECTIVE_SUB_CATEGORY_PLAGIARISM'
    OBJECTIVE_SUB_CATEGORY_PORNOGRAPHIC_DEPICTIONS = 'OBJECTIVE_SUB_CATEGORY_PORNOGRAPHIC_DEPICTIONS'
    OBJECTIVE_SUB_CATEGORY_RELIGIOUS_BELIEFS = 'OBJECTIVE_SUB_CATEGORY_RELIGIOUS_BELIEFS'
    OBJECTIVE_SUB_CATEGORY_RISKY_FINANCIAL_PRACTICES = 'OBJECTIVE_SUB_CATEGORY_RISKY_FINANCIAL_PRACTICES'
    OBJECTIVE_SUB_CATEGORY_RISKY_PRANKS = 'OBJECTIVE_SUB_CATEGORY_RISKY_PRANKS'
    OBJECTIVE_SUB_CATEGORY_SCAMS = 'OBJECTIVE_SUB_CATEGORY_SCAMS'
    OBJECTIVE_SUB_CATEGORY_SONG_LYRICS = 'OBJECTIVE_SUB_CATEGORY_SONG_LYRICS'
    OBJECTIVE_SUB_CATEGORY_SPAM = 'OBJECTIVE_SUB_CATEGORY_SPAM'
    OBJECTIVE_SUB_CATEGORY_SURVEILLANCE = 'OBJECTIVE_SUB_CATEGORY_SURVEILLANCE'
    OBJECTIVE_SUB_CATEGORY_SYSTEMIC_RACISM = 'OBJECTIVE_SUB_CATEGORY_SYSTEMIC_RACISM'
    OBJECTIVE_SUB_CATEGORY_THREATS_AND_INTIMIDATION = 'OBJECTIVE_SUB_CATEGORY_THREATS_AND_INTIMIDATION'
    OBJECTIVE_SUB_CATEGORY_TOXIC_CHEMICALS = 'OBJECTIVE_SUB_CATEGORY_TOXIC_CHEMICALS'
    OBJECTIVE_SUB_CATEGORY_UNSAFE_HEALTH_PRACTICES = 'OBJECTIVE_SUB_CATEGORY_UNSAFE_HEALTH_PRACTICES'
    OBJECTIVE_SUB_CATEGORY_WAR_CRIMES = 'OBJECTIVE_SUB_CATEGORY_WAR_CRIMES'
    OBJECTIVE_SUB_CATEGORY_WORKPLACE_DISCRIMINATION = 'OBJECTIVE_SUB_CATEGORY_WORKPLACE_DISCRIMINATION'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ObjectiveSubCategory from a JSON string"""
        return cls(json.loads(json_str))


