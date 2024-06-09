from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

import logging

from src.messages.routers import router as api_listener_router
from src.auth.routers import router as auth_router
from src.user.routers import router as user_router
import uvicorn

app = FastAPI()

app.include_router(router=api_listener_router, prefix="/messages")
app.include_router(router=user_router, prefix="/user")
app.include_router(router=auth_router, prefix="/oauth2")

logger = logging.getLogger("uvicorn.error")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred."},
    )


@app.get("/")
async def root():
    return {"message": "Hello Guys!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
