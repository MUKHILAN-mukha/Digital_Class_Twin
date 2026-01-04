from pydantic import BaseModel

class ProfileUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
