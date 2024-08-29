from pydantic import BaseModel, Field, field_validator
from typing import Optional

from .errors import BasicErrCodes, AlgorithmException


class BasicAlgorithmRequest(BaseModel):
    traceid: str = Field(default=..., title="traceId", description=f"the id to identify one single request")
    bizid: str = Field(default='-', title="bizId", description=f"the id to identify one single biz")


class BasicAlgorithmResponse(BaseModel):
    traceid: str = Field(default=..., title="traceId", description=f"the id to identify one single request")
    bizid: str = Field(default=..., title="bizId", description=f"the id to identify one single biz")
    errcode: int = 0
    errmsg: Optional[str] = None
    data: Optional[dict] = None

    @field_validator('errcode')
    def check_errcode(cls, v):
        if not BasicErrCodes.has(v):
            raise AlgorithmException(BasicErrCodes.COMMON_ERR, "undefined error code: {}".format(v))
        return v
