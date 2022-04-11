from routers import usuarios, contenidos
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from sql import models
from sql.database import engine

models.Base.metadata.create_all(bind=engine)


description = """
API MOVIES, integra un modulo de usuarios que les permite guadar sus peliculas o series favoritas
"""
# METADATA API
tags_metadata = [
    {
        "name": "Usuarios",
        "description": "Endpoints de los Usuarios",
    },
    {
        "name": "Favoritos",
        "description": "Endpoints de los favoritos",
    },
    {"name": "Seguridad", "description": "Endpoints de Seguridad"},
]

# APP
app = FastAPI(
    title="API MOVIES",
    description=description,
    version="1.0",
    openapi_tags=tags_metadata,
)

# CORS
origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONTROLLERS
app.include_router(usuarios.router)
app.include_router(contenidos.router)



