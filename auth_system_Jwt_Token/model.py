from sqlalchemy import Integer,String,engine,create_engine,MetaData
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,sessionmaker,session
from sqlalchemy.exc import IntegrityError
# password hashing file 
from passlib.context import CryptContext
from fastapi import Depends, HTTPException,status
from typing import Annotated
# from auth_system_Jwt_Token.auth.jwt_bearer import JwtBearer
# from auth_system_Jwt_Token.auth.jwt_handler import Auth
from auth.jwt_bearer import JwtBearer
from auth.jwt_handler import Auth
# from 

class Base(DeclarativeBase):
    pass

try:
    engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)
    engine.connect()
    print("connection sucessfull")
    
    
except Exception as e:
    print("connection problem !")


with Session(engine) as session:
    Session=sessionmaker(bind=engine)
    session=Session()
    
    
password_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

class User(Base):
    __tablename__='users'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    email:Mapped[str]=mapped_column(String,nullable=False,unique=True)
    password:Mapped[str]=mapped_column(String,nullable=False)
    role:Mapped[str]=mapped_column(String,default="user",nullable=False)
    contact:Mapped[int]=mapped_column(Integer,nullable=False)
    address:Mapped[str]=mapped_column(String,nullable=False)
    
    
    # password hashing 
    def get_hashed_password(password:str) ->str:
            return password_context.hash(password)
    
    #password hashing
    def verify_password(password:str,hashed_pass:str)->bool:
        return password_context.verify(password,hashed_pass)
    
    
    
    @staticmethod
    def add_user(email,password,role,contact,address):
        hashed_password=User.get_hashed_password(password)    #hash the database password while adding 
        new_user=User(email=email,password=hashed_password,role=role,contact=contact,address=address)
        
        session.add(new_user)
        
        try:
            session.commit()
            return {
                "detail":"user added sucessfully !"
            }
            
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exist ")
    
    
    @staticmethod    
    def get_current_user(token:str=Depends(JwtBearer())):
        user_email = Auth.decode_generate_token(token)
        if not user_email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user=session.query(User).filter_by(email=user_email['email']).first()
        
        if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")  
        # Return the user's email and the role
        return{"email":user.email,"role":user.role} 

    
# class RoleChecker:
#     def __init__(self,allowed_roles) :
#         self.allowed_roles=allowed_roles
        
#     def __call__(self,user=Depends(User.get_current_user)):
        
#         if user.get('role') in self.allowed_roles:
#             return True
        
#         else:
#             raise HTTPException(status_code=401,detail="You don't have enough permissions ")

    
