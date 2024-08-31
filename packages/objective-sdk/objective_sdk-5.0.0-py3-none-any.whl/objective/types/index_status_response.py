# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["IndexStatusResponse", "Status"]


class Status(BaseModel):
    error: float = FieldInfo(alias="ERROR")

    processing: float = FieldInfo(alias="PROCESSING")

    ready: float = FieldInfo(alias="READY")

    uploaded: float = FieldInfo(alias="UPLOADED")


class IndexStatusResponse(BaseModel):
    status: Status
