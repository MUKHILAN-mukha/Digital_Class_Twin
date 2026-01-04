from pydantic import BaseModel


class LinkChildRequest(BaseModel):
    child_id: str
