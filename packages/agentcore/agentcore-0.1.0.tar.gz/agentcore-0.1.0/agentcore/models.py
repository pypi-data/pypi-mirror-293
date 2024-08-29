from typing import Optional

from pydantic import BaseModel


class V1UserProfile(BaseModel):
    email: str
    display_name: Optional[str] = None
    handle: Optional[str] = None
    picture: Optional[str] = None
    created: Optional[int] = None
    updated: Optional[int] = None
    token: Optional[str] = None
