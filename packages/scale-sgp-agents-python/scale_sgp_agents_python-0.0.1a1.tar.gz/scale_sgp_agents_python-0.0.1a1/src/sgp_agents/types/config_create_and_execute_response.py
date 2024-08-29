# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .execution_sync_response import ExecutionSyncResponse
from .execution_stream_response import ExecutionStreamResponse

__all__ = ["ConfigCreateAndExecuteResponse"]

ConfigCreateAndExecuteResponse: TypeAlias = Union[ExecutionSyncResponse, ExecutionStreamResponse]
