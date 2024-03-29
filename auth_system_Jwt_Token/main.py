from fastapi import FastAPI,HTTPException,status,Depends
from typing import Annotated
from pydantic import  BaseModel
from model import User,session
from auth.jwt_handler import Auth
from auth.jwt_bearer import JwtBearer
# from role_check import RoleChecker

app=FastAPI(title="Token Authentication ")

#pydantic models 
class RegisterUser(BaseModel):
    email:str
    password:str
    role:str |None
    contact:int
    address:str
    
class LoginUser(BaseModel):
    email:str
    password:str



# from typing import Annotated
# from model import User
# from fastapi import Depends,HTTPException,status
# from main import get_current_user






# register
@app.post("/register")
async def register(signin:RegisterUser):
    
    new_user=User.add_user(email=signin.email,password=signin.password,role=signin.role,contact=signin.contact,address=signin.contact)
    return new_user

# login
@app.post("/login")
async def login(data:LoginUser):
    user=session.query(User).filter_by(email=data.email).first()
    
    if user and User.verify_password(data.password,user.password):
       
        token=Auth.generate_token(email=data.email)
        return token
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email and password !")
        
# get current user

@app.get("/users/me")
def get_current_user(token:str=Depends(JwtBearer())):
    user_email = Auth.decode_generate_token(token)
    if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    # Query the database to get the user by email   
    user=session.query(User).filter_by(email=user_email["email"]).first()
    
    if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")  
     # Return the user's email
    return{"email":user.email,"role":user.role} 
 


#TODO: 1. dependences lagayera validation lagaune , ani authorised bahek le acess na paune , tespaxi ko kam chai current user get garne ho token halera login gareko manxe lai herna milne banaune kam ho ,teti garepaix chai authentication ko part j hos sakeyo
# TODO:2 yesma chai aba role based rakhdine ho 3 ota different users haru lai rakhdine ho ani vaihalxa aajha ko task 
#TODO:3 aajha (Teakbreak) baje samma ma chai yo sabai kura sakkaune ho   nearly 4 baje samma garna pahine 
#TODO: 4 Logger implementation garne ho majjale chai hai ta  (Basic of log implementation garne ho majjale chai )

class RoleChecker:
    def __init__(self,allowed_roles) :
        self.allowed_roles=allowed_roles
        
    def __call__(self,user=Depends(get_current_user)):
        print(user)
        if user.get('role') in self.allowed_roles:
            return True
        else:
            raise HTTPException(status_code=401,detail="You don't have enough permissions ")


@app.get("/name/")

async def get_name(_:bool=Depends(RoleChecker(allowed_roles=["admin"]))):
    return f"Hello  GoodMorning !"






