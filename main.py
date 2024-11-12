from fastapi import Response, UploadFile, File, Depends, FastAPI, Depends, Request, APIRouter
from tortoise.contrib.fastapi import register_tortoise, RegisterTortoise
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
import asyncio, os, logging, uvicorn, json, time, subprocess, sys
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise, generate_config
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dotenv import load_dotenv
from app import *
from pydantic import BaseModel
from app.schemas.api_response import ApiResponse
from app.middlewares import add_process_time_header
from app.utils.jwt_auth import get_user
from app.api import router


load_dotenv()
prefix = os.getenv("PREFIX")


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    # await FastAPILimiter.init(App().get_redis(sync=False))
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    # loop.create_task(run_schedule())
    yield
    await Tortoise.close_connections()


class CustomAPIRouter(APIRouter):
    def api_route(self, path: str, *, response_model=ApiResponse, **kwargs):
        return super().api_route(path, response_model=response_model, **kwargs)


app = FastAPI(
    debug=True if os.getenv("RUNNING_MODE") == "dev" else False,
    dependencies=[Depends(get_user)],
    lifespan=lifespan,
    docs_url=f"{prefix}/docs",
)


app.middleware("http")(add_process_time_header)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content=jsonable_encoder(
#             ApiResponse(
#                 status=False, message="پارامتر های ورودی معتبر نیست", data=exc.errors()
#             )
#         ),
#     )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coustom_router = CustomAPIRouter(prefix="/sims")


app.include_router(coustom_router)
app.include_router(router)



@app.get(f"/", include_in_schema=False)
async def root():
    return f"APP IS RUNNING !"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT")),
        log_level=logging.WARNING if os.getenv("RUNNING_MODE") == "prod" else logging.INFO,
        workers=2 if os.getenv("RUNNING_MODE") == "dev" else 1,
        reload=True,
    )
