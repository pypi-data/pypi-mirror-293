# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ExecutionStreamResponse", "MessageChunk", "MessageChunkLogprobs", "ResponseStatus"]


class MessageChunkLogprobs(BaseModel):
    token: str

    logprob: float


class MessageChunk(BaseModel):
    content: str

    role: str

    finish_reason: Optional[Literal["stop", "length", "content_filter", "tool_calls"]] = None

    logprobs: Optional[MessageChunkLogprobs] = None


class ResponseStatus(BaseModel):
    request_id: str

    status: Literal["in-progress", "success", "error"]

    error_message: Optional[str] = None

    timestamp: Optional[datetime] = None


class ExecutionStreamResponse(BaseModel):
    message_chunk: MessageChunk

    response_status: ResponseStatus

    run_id: str

    run_status: Literal["completed", "user_request"]
    """An enumeration."""

    metadata: Optional[object] = None
