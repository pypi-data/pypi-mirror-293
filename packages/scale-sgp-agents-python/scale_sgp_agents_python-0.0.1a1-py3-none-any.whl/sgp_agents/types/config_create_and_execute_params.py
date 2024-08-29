# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .plan_config_param import PlanConfigParam
from .workflow_config_param import WorkflowConfigParam

__all__ = ["ConfigCreateAndExecuteParams", "Config", "Message"]


class ConfigCreateAndExecuteParams(TypedDict, total=False):
    config: Required[Config]

    messages: Required[Iterable[Message]]

    session_id: Required[str]

    id: str

    metadata: object

    stream: bool


Config: TypeAlias = Union[PlanConfigParam, WorkflowConfigParam]


class Message(TypedDict, total=False):
    role: Required[Literal["model", "user", "system"]]

    text: Required[str]

    uuid: Annotated[str, PropertyInfo(alias="UUID")]
