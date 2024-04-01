from fastapi import HTTPException,Depends
from model import User
class RoleChecker:
    def __init__(self,allowed_roles) :
        self.allowed_roles=allowed_roles
        
    def __call__(self,user=Depends(User.get_current_user)):
        
        if user.get('role') in self.allowed_roles:
            return True
        
        else:
            raise HTTPException(status_code=401,detail="You don't have enough permissions ")
