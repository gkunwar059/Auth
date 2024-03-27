from sqlalchemy import Integer,String,engine,create_engine,MetaData
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,sessionmaker,session
# from decouple import config


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
    


class User(Base):
    __tablename__='users'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    email:Mapped[str]=mapped_column(String,nullable=False)
    password:Mapped[str]=mapped_column(String,nullable=False)
    contact1:Mapped[int]=mapped_column(String,nullable=True)
    contact2:Mapped[int]=mapped_column(String,nullable=True)
    # contact3:Mapped[int]=mapped_column(String,nullable=True)
    