from pydantic import BaseModel, Field

class RegisterUser(BaseModel):
    email: str
    password: str
    role_id: str


class LoginUser(BaseModel):
    email: str
    password: str


class TokenID(BaseModel):
    token: str


class RoleAssignPermission(BaseModel):
    role_id: int
    permission_id: int


class ForgetPassword(BaseModel):
    email:str
    
    
class UserChangePassword(BaseModel):
    old_password:str
    new_password:str