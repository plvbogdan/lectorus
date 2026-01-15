import jwt
from dotenv import load_dotenv
import os
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

http_bearer = HTTPBearer()

load_dotenv()

SECRET_KEY = str(os.getenv("SECRET_KEY"))

def encode_jwt(user_id, email):
    data = {
        "user_id": user_id,
        "user_email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None
    

def get_current_user_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
    token = credentials.credentials
    payload = decode_jwt(token)
    return payload