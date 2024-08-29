# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ExecutionSyncResponse", "Message", "ResponseStatus", "Usage"]


class Message(BaseModel):
    role: Literal["model", "user", "system"]

    text: str

    uuid: Optional[str] = FieldInfo(alias="UUID", default=None)


class ResponseStatus(BaseModel):
    request_id: str

    status: Literal["in-progress", "success", "error"]

    error_message: Optional[str] = None

    timestamp: Optional[datetime] = None


class Usage(BaseModel):
    completion_tokens: int

    prompt_tokens: int

    total_tokens: int


class ExecutionSyncResponse(BaseModel):
    message: Message

    response_status: ResponseStatus

    run_id: str

    run_status: Literal["completed", "user_request"]
    """An enumeration."""

    metadata: Optional[object] = None

    usage: Optional[Usage] = None
