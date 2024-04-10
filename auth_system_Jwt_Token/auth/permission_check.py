from typing import Any,List
from model import User,Role
from fastapi import Depends,HTTPException

class PermissionCheck:
    def __init__(self,allowed_permission:List[str]):
        self.allowed_permission=allowed_permission
        
    def __call__(self,user=Depends(User.current_user)):
     
        user_permissions=Role.get_permission_role(user['role'])
       
        for permission  in self.allowed_permission:                                                                                       #existing permission in allowed permission ma xa vane chai user return garne ho 
                                                                     
            if permission not in user_permissions:                                                                                           #if permission xaina vane chai  exception aaunxa 
    
                raise HTTPException(status_code=401,detail="You don't have permission to access ! ")
    
    
        return user
    
        
        
