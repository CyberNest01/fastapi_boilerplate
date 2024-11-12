import hashlib, time, jwt, os
from nanoid import generate 
import time
from fastapi import Header, Request
from fastapi.exceptions import HTTPException
from starlette.datastructures import MutableHeaders
from dotenv import load_dotenv
from app.models.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
prefix="" if os.getenv("RUNNING_MODE")=="dev" else f'/{os.getenv("PREFIX")}'

def jwt_generator(username):
    return jwt.encode({"username":username, "expire":(time.time() + os.getenv("JWT_EXPIRE_TIME"))}, SECRET_KEY, algorithm="HS256")

def hash_saz(text):
    return hashlib.sha256(text.encode()).hexdigest()

def decode_jwt(token):
    return jwt.decode(token.encode(), SECRET_KEY, algorithms=["HS256"])

def generate_id(size=10):
    return generate(size=size)

def get_user(request: Request, HTTP_AUTHORIZATION:str = Header("Bearer token")):
    if (request.url._url.split(prefix)[1] if prefix else request.url.path) not in ["/", "/v1/users/login", "/docs", "/redoc", "/openapi.json"]:
        if os.getenv('RUNNING_MODE') == "dev" and HTTP_AUTHORIZATION.replace("Bearer ", "") == os.getenv("DEV_JWT"):
            jwt_opened = {"username":os.getenv("DEV_USERNAME"), "expire":(time.time() + int(os.getenv("JWT_EXPIRE_TIME")))}
        else:
            try:
                jwt_opened = decode_jwt(HTTP_AUTHORIZATION.replace("Bearer ", ""))
            except:
                try:
                    jwt_opened = decode_jwt(request.headers["authorization"].replace("Bearer ", ""))
                except:
                    raise HTTPException(401, detail="not authenticate")
            if jwt_opened["expire"] < time.time():
                raise HTTPException(401, detail="token is expire")
        # if "user_id" not in jwt_opened:
        #     raise HTTPException(401, detail="jwt does not have user_id")
        new_header = MutableHeaders(request._headers)
        new_header["username"]=jwt_opened["username"]
        request._headers = new_header
        if jwt_opened['username'] == os.getenv("DEV_USERNAME"):
            return User.filter(username="debug").first()
        return User.filter(username=jwt_opened["username"])