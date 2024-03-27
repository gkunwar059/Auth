from sqlalchemy import Integer,String,engine,create_engine,MetaData
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,sessionmaker,session
# from decouple import config
from passlib.context import CryptContext


# DATABASE_CONNECTION=config('DATABASE')
class Base(DeclarativeBase):
    pass

try:
    # engine=create_engine(DATABASE_CONNECTION,echo=True)
    engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)
    engine.connect()
    print("connection sucessfull")
    
    
except Exception as e:
    print("connection problem !")


with Session(engine) as session:
    Session=sessionmaker(bind=engine)
    session=Session()

pwt_context=CryptContext(schemes=["bcrypt"],deprecated='auto')




class Users(Base):
    __tablename__='user'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    username:Mapped[str]=mapped_column(String,nullable=False,unique=True)
    password:Mapped[str]=mapped_column(String,nullable=False,unique=True)
    
    @staticmethod
    def verify_password(plain_password,hash_password):
        return pwt_context.verify(plain_password,hash_password)
    
    @staticmethod
    def get_password_hash(password):
        return pwt_context.hash(password)

    @staticmethod
    def add_user(username,password):
        hash_password=Users.get_password_hash(password)       #things to know 
        new_member=Users(username=username,password=hash_password)              #thinks to remember the concept and implementations

        session.add(new_member)
        session.commit()
    

    def autheticate_user(username,password):
        user= session.query(Users).filter_by(username=username,password=password).first()
        
        # if user and Users.verify_password(password,user.password) :
        #     return user
        
        # return None
        # if user:
        
        return user
            
        
        
        
        # ======================================================================
        # another code here 
        # Implementing Basic Authentication With Python FastAPI
from fastapi import FastAPI,Depends,HTTPException, Request,status
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import uvicorn
from model import Users
from pydantic import BaseModel

class UserRegister(BaseModel):
    username:str
    password:str
    
    




# app = FastAPI()
security=HTTPBasic()
# app=FastAPI(dependencies=[Depends(security)])           # this method can be also applied too 
app=FastAPI()

    #Fake Databse
# users={
    
#     "admin":{
#         "password":"ganesh@123",
#         "token":"",
#         "priviliged":True
#     }
    
# }
# Next, we want to create an authentication method that will search
# the dictionary and verify the username and password.

def authencated_user(creds:HTTPBasicCredentials=Depends(security)):
    username=creds.username
    password=creds.password

    # if username in users and password==users[username]["password"]:
                                                   #this commented for the fake dummy database
        # print("User Validated")
        # return True
    new_user=Users.autheticate_user(username=username,password=password)
    
    if new_user:
        return new_user
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or Password !",headers={"WWW-Authenticate":"Basic"},)
    
    
    # Now, we can create our path operation function and check 
    # for proper authentication using the following code:
    
    
@app.get("/name/{name}",dependencies=[Depends(authencated_user)])
async def search(name:str,request:Request):
    print(request.__dict__)
    return(f"Hello {name} G ")
    
    
@app.post("/register")

async def register(register:UserRegister):
    new_user=Users.add_user(register.username,register.password)
    if not new_user:
        return {
            "details":"User added Sucessfully !"
        }
   
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Registered Failed ")
        
if __name__ == "__main__":
    uvicorn.run("basic_auth:app", host="127.0.0.1", port=8000, reload=True)
      
   
       

       