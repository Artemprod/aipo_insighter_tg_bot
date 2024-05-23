from typing import Optional

from pydantic import BaseModel


class ResponseText(BaseModel):
    id: int | str
    initiator_user_id: int

