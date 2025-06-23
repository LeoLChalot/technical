from fastapi import FastAPI, Depends

# Modifiez cette partie
from .dependencies import get_query_token
from .settings import settings
from .routers import projects # Importez le nouveau routeur

app = FastAPI(dependencies=[Depends(get_query_token)])

# app = FastAPI()

# Incluez le routeur dans l'application principale
app.include_router(projects.router, prefix=settings.prefix)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}