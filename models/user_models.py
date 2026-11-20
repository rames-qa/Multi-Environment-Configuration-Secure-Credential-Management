from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str
