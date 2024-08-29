# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .plan_config_param import PlanConfigParam
from .workflow_config_param import WorkflowConfigParam

__all__ = ["ConfigCreateParams", "Config"]


class ConfigCreateParams(TypedDict, total=False):
    config: Required[Config]


Config: TypeAlias = Union[PlanConfigParam, WorkflowConfigParam]
