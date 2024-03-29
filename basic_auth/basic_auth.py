# Implementing Basic Authentication With Python FastAPI
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from model import Users
from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str


security = HTTPBasic()
app = FastAPI()


def authencated_user(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    password = creds.password
    return Users.autheticate_user(username=username, password=password)
    

@app.get("/name/{name}", dependencies=[Depends(authencated_user)])
async def search(name: str):
    return f"Hello {name} G "

@app.post("/register")
async def register(register: UserRegister):
    new_user = Users.add_user(register.username, register.password)
    if not new_user:
        return {"details": "User added Sucessfully !"}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Registered Failed "
        )

if __name__ == "__main__":
    uvicorn.run("basic_auth:app", host="127.0.0.1", port=8000, reload=True)
