# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Union
from promptflow.core import tool
from promptflow.connections import AzureAIServicesConnection, CustomConnection
from language_utils.language_skill import LanguageSkill
from language_utils.language_tool_utils import run_language_skill

API_VERSION = "2023-11-15-preview"
SKILL = LanguageSkill.LANGUAGE_DETECTION


@tool
def get_language_detection(
        connection: Union[AzureAIServicesConnection, CustomConnection],
        text: str,
        max_retries: int = 5,
        max_wait: int = 60,
        parse_response: bool = False):
    # Create input:
    document = {"text": text, "id": "1"}

    # Create query parameters:
    query_parameters = {
        "api-version": API_VERSION,
    }

    # Create task parameters:
    task_parameters = {}

    # Create skill config:
    skill_config = {
        "connection": connection,
        "query_parameters": query_parameters,
        "input": document,
        "task_parameters": task_parameters,
        "skill": SKILL,
        "max_retries": max_retries,
        "max_wait": max_wait,
        "parse_response": parse_response
    }

    # Run skill:
    return run_language_skill(skill_config=skill_config)
