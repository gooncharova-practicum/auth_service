from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    data: Any = None
    success: bool = True
    error: Any = None
