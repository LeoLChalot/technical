from fastapi import FastAPI, Depends

from .dependencies import get_query_token
from .settings import settings


app = FastAPI(dependencies=[Depends(get_query_token)])


# app.include_router(users.router, prefix=settings.prefix)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
