from sqlalchemy import Integer, String, engine, create_engine, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    sessionmaker,
    session,
)
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError

# from decouple import config
from passlib.context import CryptContext


# DATABASE_CONNECTION=config('DATABASE')
class Base(DeclarativeBase):
    pass


try:
    # engine=create_engine(DATABASE_CONNECTION,echo=True)
    engine = create_engine(
        "postgresql://postgres:123456789@127.0.0.1:5432/postgres", echo=False
    )
    engine.connect()
    print("connection sucessfull")


except Exception as e:
    print("connection problem !")


with Session(engine) as session:
    Session = sessionmaker(bind=engine)
    session = Session()

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Users(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwt_context.verify(plain_password, hash_password)

    @staticmethod
    def get_password_hash(password):
        return pwt_context.hash(password)
    

    @staticmethod
    def add_user(username, password):
        hash_password = Users.get_password_hash(password)  # things to know
        new_member = Users(
            username=username, password=hash_password
        )  # thinks to remember the concept and implementations
        
        session.add(new_member)
      
        # uniquee value integrity deals with the duplicate value 
        try:
            session.commit()
        except IntegrityError :
            session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Username already exists!")
   
    @staticmethod
    def autheticate_user(username, password):
        user = session.query(Users).filter_by(username=username).first()
        
        if user and Users.verify_password(password,user.password):        #verify garne kam garxa ke hash vayeko password na normal password lai 
            return user
        
        else:
            raise HTTPException(status_code=401,detail="invalid credientials !")


