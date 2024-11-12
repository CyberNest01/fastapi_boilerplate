from typing import Any, Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    status: bool
    message: Optional[str] = None
    data: Any