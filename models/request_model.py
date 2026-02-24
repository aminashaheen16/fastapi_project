from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: str
    username: str
    email: str