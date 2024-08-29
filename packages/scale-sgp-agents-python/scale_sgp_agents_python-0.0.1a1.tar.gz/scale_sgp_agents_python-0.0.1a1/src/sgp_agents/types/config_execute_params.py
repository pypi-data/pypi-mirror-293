# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ConfigExecuteParams", "Message"]


class ConfigExecuteParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]

    session_id: Required[str]

    id: str

    metadata: object

    run_id: str

    stream: bool


class Message(TypedDict, total=False):
    role: Required[Literal["model", "user", "system"]]

    text: Required[str]

    uuid: Annotated[str, PropertyInfo(alias="UUID")]
