import os
from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import HTTPException, status


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 MIN
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 DAYS

ALGORITHM = "HS256"
JWT_SECRET_KEY = "91346c3609fb8bfe73f8331aca5648c943cff07dea56a1edd5dfe60c84560e78"
JWT_REFRESH_SECRET_KEY = (
    "14b9f5e27d3c67159ae71bdabf00585c7040249f8aa68f8f90b15931a005d724"
)

class Auth:

    @staticmethod
    def generate_token(email):

        access_payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        refresh_payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        }

        access_token = jwt.encode(access_payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(
            refresh_payload, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM
        )

        return {"access_token": access_token, "refresh_token": refresh_token}

    def decode_generate_token(token):
        try:
            decoded_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_data

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=" Token Expired !"
            )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=" Invalid  Token !"
            )



