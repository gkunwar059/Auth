# from typing import Annotated
# from model import User
# from fastapi import Depends,HTTPException,status
# from main import get_current_user

# class RoleChecker:
#     def __init__(self,allowed_roles) :
#         self.allowed_roles=allowed_roles
        
#     def __call__(self,user:Annotated[User,Depends(get_current_user)]):
#         if user.role in self.allowed_roles:
#             return True
#         else:
#             raise HTTPException(status_code=401,detail="You don't have enough permissions ")