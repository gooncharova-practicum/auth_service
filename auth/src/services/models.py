from typing import Any

from pydantic import BaseModel


class ServiceResult(BaseModel):
    data: Any | None
    error_message: str | None
    success: bool
