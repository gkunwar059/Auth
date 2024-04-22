from fastapi import FastAPI, HTTPException, status, Depends, Request, Form
from typing import Annotated

# from model import User, session,Select
from auth.jwt_handler import Auth
from auth.jwt_bearer import JwtBearer
from auth.permission_check import PermissionCheck
from model import User, Permission, Role, session, Select
from schemas import (
    RegisterUser,
    LoginUser,
    RoleAssignPermission,
    ForgetPassword,
    UserChangePassword,
)
import uuid
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from email_notification.notify import (
    send_registration_notification,
    send_reset_password_mail,
)

app = FastAPI(title="Role Based Access Control ")
from model import log_request_response, Request, Response


parent_directory = Path(__file__).parent
templates_path = parent_directory.parent / "templates"
templates = Jinja2Templates(directory=templates_path)


# register
@app.post("/register")
async def register(signin: RegisterUser, request: Request):

    new_user = User.add_user(
        email=signin.email, password=signin.password, role_id=signin.role_id
    )
    await log_request_response(
        request, Response(status_code=status.HTTP_201_CREATED), data=new_user
    )

    return new_user
    # return {**signin.dict()}    #response the data similar databasez


# ================================================================================================
@app.get("/user")
async def get_user(request: Request):
    user = session.query(User).all()
    await log_request_response(
        request,
        Response(status_code=status.HTTP_201_CREATED),
        data=[user_details.__dict__ for user_details in user],
        # data=user.dict(),
    )
    return user


# ----> make password as a defer column to exclude the password right
# =================================================================
# login
@app.post("/login")
async def login(data: LoginUser):
    user = session.query(User).filter_by(email=data.email).first()

    if user and User.verify_password(data.password, user.password):

        token = Auth.generate_token(email=data.email)
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email and password !",
        )


"""'
make a automatic current user here out of the code below 

"""


@app.post("/change-password")
async def change_password(
    change_password: UserChangePassword, user: User = Depends(User.current_user)
):

    # check user
    user = session.query(User).filter_by(email=user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found !"
        )

    if not User.verify_password(
        change_password.old_password, user.password
    ):  # check old password that i have enter with the password in the dataabase
        raise ValueError(f" old password provided doesn't match,please try again !")
        # after the above condtion true hash the newpassword and save into the database (such a simple way of change the change password)
    user.password = User.get_hashed_password(change_password.new_password)
    session.commit()
    return {"message": "password changed sucessfully !"}


@app.post("user/reset_password")
def user_reset_password(request: Request, new_password: str = Form(...)):
    """ "
    Resets password for a user
    """
    user = session.query(User).filter_by(email=user.email).first()
    try:
        result = User.user_reset_password(user.email, new_password)
        return templates.TemplateResponse(
            "reset_password_result.html", {"request": request, "sucess": result}
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexcepted error occured .Report this message to support :{e}",
        )


@app.get(
    "/users/me/reset_password_template",
    response_class=HTMLResponse,
    summary="Reset password for a user",
    tags=["Users"],
)
def user_reset_password_template(
    request: Request, user: User = Depends(User.current_user)
):
    """
    Resets password for a user.
    """
    try:
        token = request.query_params.get("access_token")
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "user": user, "access_token": token},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@app.post("/users/me/forgot_password", tags=["Users"])
async def user_forgot_password(request: Request, user_email: str):
    """
    Triggers forgot password mechanism for a user.
    """
    TEMP_TOKEN_EXPIRE_MINUTES = 10
    try:
        user = session.query(User).filter_by(email=user_email["email"])
        if user:
            access_token = Auth.generate_token(
                data=user_email, expire_minutes=TEMP_TOKEN_EXPIRE_MINUTES
            )
            url = f"{request.base_url}v1/users/me/reset_password_template?access_token={access_token}"
            await send_reset_password_mail(
                recipient_email=user_email,
                user=user,
                url=url,
                expire_in_minutes=TEMP_TOKEN_EXPIRE_MINUTES,
            )
        return {
            "result": f"An email has been sent to {user_email} with a link for password reset."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@app.post("/current_user")
async def current_user(token: str = Depends(JwtBearer())):
    new_user = User.current_user(token)
    return new_user


@app.get("/")
async def home():
    return {"Hello Ganesh Kunwar , Welcome to Auth  !!"}


@app.get(
    "/name/",
    dependencies=[
        Depends(PermissionCheck(allowed_permission=["admin:all", "user:all"]))
    ],
)
async def get_name():
    return f"Hello  GoodMorning !"


@app.get("/member/", dependencies=[Depends(JwtBearer())])
async def get_member():
    return f"Hello  Member !"


@app.post("/role/assignpermission", tags=["Role"])
async def assign_permission_to_role(assign: RoleAssignPermission):
    success = Permission.assign_permission_role(
        role_id=assign.role_id, permission_id=assign.permission_id
    )

    if success:
        return {"message": "Permission assigned to role successfully"}
    else:
        raise HTTPException(status_code=404, detail="Role or permission not found")


# @app.patch("/user/change-password")
# async def change_password(
#     changepassword: ChangePassword, current_user=Depends(current_user)
# ):
#     user = session.query(User).filter_by(email=User.email).first()
#     print(user)
#     if not user:
#         raise HTTPException(status_code=404, detail="user not found !")

#     if not User.verify_password(changepassword.current_password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect password")
