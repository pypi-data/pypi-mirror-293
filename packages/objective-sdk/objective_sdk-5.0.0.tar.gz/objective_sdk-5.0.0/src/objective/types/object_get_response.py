# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ObjectGetResponse", "Status", "StatusIndex"]


class StatusIndex(BaseModel):
    id: str

    status: Literal["UPLOADED", "PROCESSING", "READY", "ERROR"]


class Status(BaseModel):
    indexes: List[StatusIndex]


class ObjectGetResponse(BaseModel):
    id: str

    status: Status

    object: Optional[builtins.object] = None
