#the function of this file is to check whether  the request is authorized or not [verification of route ] 

from typing_extensions import Annotated, Doc
from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from auth.jwt_handler import Auth

class JwtBearer(HTTPBearer):  #takes as amain parameter or arg

    def __init__(self,auto_error:bool=True):
        super().__init__(auto_error=auto_error)
        
        
    async def __call__(self,request:Request):
        credentials:HTTPAuthorizationCredentials= await super(JwtBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme=="Bearer":
                raise HTTPException(status_code=403,detail="Invalid or expired token !")
            return credentials.credentials
        
        else:
            raise HTTPException(status_code=403,detail="Invalid or expired token !")
            
    def verify_jwt(self,jwtoken:str):
        isTokenValid:bool=False     #a false flag
        payload=Auth.decode_generate_token(jwtoken)
        if payload:
            isTokenValid=True
        return isTokenValid
        
        
        