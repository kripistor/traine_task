from fastapi import FastAPI, HTTPException
from async_fastapi_jwt_auth.exceptions import MissingTokenError, AuthJWTException, JWTDecodeError
from starlette.responses import JSONResponse

from app.factory import create_app
from app.core.logger import logger

app = create_app()


@app.exception_handler(JWTDecodeError)
async def jwt_decode_exception_handler(request, exc):
    return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})


@app.exception_handler(MissingTokenError)
async def missing_token_exception_handler(request, exc):
    raise HTTPException(status_code=401, detail="Token is missing")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn in reload mode")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8001"),
    )
