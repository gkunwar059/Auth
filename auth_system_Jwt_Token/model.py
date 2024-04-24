from sqlalchemy import (
    Integer,
    Select,
    String,
    engine,
    create_engine,
    MetaData,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    sessionmaker,
    session,
    relationship,
)

from sqlalchemy.exc import IntegrityError

# password hashing file
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from typing import Annotated

# from auth_system_Jwt_Token.auth.jwt_bearer import JwtBearer
# from auth_system_Jwt_Token.auth.jwt_handler import Auth
from auth.jwt_bearer import JwtBearer
from auth.jwt_handler import Auth

# for the logger in python
from fastapi import FastAPI, status, Request, Response
from typing import Any
import json  # For JSON serialization

# configuring logging
import logging

logger = logging.getLogger(
    __name__
)  # Adjusting logging level as need (eg:DEBUG for more details )

logger.setLevel(logging.INFO)
handler = logging.StreamHandler()  # log the console by default
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# =============================IMPORTANT LOGGER CONCEPT IN FASTAPI ===============================


async def log_request_response(request: Request, response: Response, data: Any):
    """Logs request and response details for a FastAPI endpoint."""
    logger.info(f"---Request---")
    logger.info(f"Method:{request.method}")
    logger.info(f"URL:{request.url}")

    # log response details
    logger.info(f"---Response ---")
    logger.info(f"Status code :{response.status_code}")
    logger.info(f"Response data :{data}")


# ===================================================================================================


class Base(DeclarativeBase):
    pass


try:
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


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "testuser"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    images: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
    roles = relationship("Role", back_populates="users")

    # password hashing
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)

    # password hashing
    def verify_password(password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    @staticmethod
    def add_user(email, password, images, role_id):
        hashed_password = User.get_hashed_password(
            password
        )  # hash the database password while adding
        new_user = User(
            email=email, images=images, password=hashed_password, role_id=role_id
        )

        session.add(new_user)
        try:
            session.commit()

            return {"detail": "user added sucessfully !"}

        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exist "
            )

    @staticmethod
    def current_user(token: str = Depends(JwtBearer())):
        user_email = Auth.decode_generate_token(token)

        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid Token !")

        user = session.query(User).filter_by(email=user_email["email"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not Found !")

        return {"email": user.email, "role": user.role_id}

    @staticmethod
    def user_reset_password(email: str, new_password: str):
        try:
            user = session.query(User).filter(User.email == email).first()
            user.password = User.get_hashed_password(new_password)
            session.commit

        except Exception:
            return False

        return True


class RolePermission(Base):
    __tablename__ = "role_permission"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("permissions.id"))


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    users = relationship("User", back_populates="roles")

    permissions = relationship(
        "Permission", secondary="role_permission", back_populates="roles"
    )

    @staticmethod
    def get_permission_role(
        role_id,
    ):  # NOTE:role ma vayeko permission haru lai print garne (role_id ma assign vayeko kura ko chai list of permiison haru rakheko xa )
        permission_role = session.query(RolePermission).filter_by(role_id=role_id).all()

        permissions = []
        for role in permission_role:
            permissions.append(Permission.get_name_from_id(role.permission_id))

        return permissions


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    p_name: Mapped[str] = mapped_column(nullable=False)
    roles = relationship(
        "Role", secondary="role_permission", back_populates="permissions"
    )

    @staticmethod
    def assign_permission_role(role_id, permission_id):
        permission = session.query(Permission).get(permission_id)
        role = session.query(Role).get(role_id)

        if permission and role:
            role.permissions.append(permission)
            session.commit()
            return True

        else:
            return False

    @staticmethod
    def get_permission(permission_id):  # NOTE:permission id
        return session.query(Permission).filter_by(id=permission_id).all()

    @classmethod
    def get_name_from_id(
        cls, permission_id
    ):  # NOTE:permission id bata chai name call garne permisison name
        return session.scalar(Select(cls.p_name).where(cls.id == permission_id))
