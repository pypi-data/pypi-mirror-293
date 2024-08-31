# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["IndexStatusByTypeResponse", "Status"]


class Status(BaseModel):
    error: Optional[float] = FieldInfo(alias="ERROR", default=None)

    processing: Optional[float] = FieldInfo(alias="PROCESSING", default=None)

    ready: Optional[float] = FieldInfo(alias="READY", default=None)

    uploaded: Optional[float] = FieldInfo(alias="UPLOADED", default=None)


class IndexStatusByTypeResponse(BaseModel):
    status: Status
