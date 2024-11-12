from app.schemas.api_response import ApiResponse
from app.api import router
from db_config import TORTOISE_ORM

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
import asyncio
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from dotenv import load_dotenv

from starlette.responses import JSONResponse
from starlette import status
from contextlib import asynccontextmanager
import os


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.get_event_loop()
    await Tortoise.init(config=TORTOISE_ORM)

    yield

    await Tortoise.close_connections()


app = FastAPI(debug=os.getenv("DEBUG"), lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ApiResponse(
                status=False, message="پارامتر های ورودی معتبر نیست", data=exc.errors()
            )
        ),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
