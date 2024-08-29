from typing import Any, Dict, TypeVar

T = TypeVar("T", bound="EndpointMessageOutPayload")

EndpointMessageOutPayload = Dict[str, Any]
