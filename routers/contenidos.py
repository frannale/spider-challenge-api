import os

from dotenv import dotenv_values
from cachetools import cached, TTLCache

from fastapi import APIRouter, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

import sql.schemas.contenidos as ContenidoSchema
import sql.schemas.responses as ResponseSchema

import urllib.parse
import urllib.request, json 



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

BASEDIR = os.path.abspath(os.path.dirname("./"))

config = dotenv_values(os.path.join(BASEDIR, ".env"))

@router.get(
    "/contenidos",
    response_model=ContenidoSchema.GetContenidos,
    description="Retorna las peliculas y series mas populares",
    responses={500: {"model": ResponseSchema.MensajeError500}},
    tags=["Contenido"],
)
async def Get_Contenidos_Populares(
    request: Request,
):
 
    try:
        tipo = request.query_params.get('tipo','all')
        contenidos = get_contenido_popular(tipo)
        
        return {"code": 200, "contenidos": contenidos }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/contenidos/{id_contenido}",
    response_model=ContenidoSchema.GetContenido,
    description="Retorna la información del contenido",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Contenido"],
)
def Get_Contenido(
    id_contenido: int
):

    try:
        contenido = None
        if contenido == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un contenido registrado",
                },
            )
        else:
            return {
                "code": 200,
                "contenido": contenido
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


# CACHEA RESULTADO DE ULTIMAS 50 POR 1 HORA
cache = TTLCache(maxsize=50, ttl=3600)

@cached(cache)
def get_contenido_popular(type : str):

    # AUTENTICACION EN API MOVIE DB
    url = config["API_URL"] + 'trending/' + type + '/day?api_key=' + config["API_KEY"]
    request = urllib.request.Request(url)
    request.add_header("Content-Type", "application/json")
    
    with urllib.request.urlopen(request) as url:
        data = json.loads(url.read().decode())

    contenidos = []
    for media in data["results"]:
        if media["media_type"] == "movie":
            # PARSEA PELICULA
            current_contenido = {
                "nombre" : media["original_title"],
                "tipo" : "MOVIE",
                "poster" : "https://image.tmdb.org/t/p/original" + media["poster_path"]
            }
        else:
            # PARSEA TV SHOW
            current_contenido = {
                "nombre" : media["original_name"],
                "tipo" : "TV - SHOW",
                "poster" : "https://image.tmdb.org/t/p/original" + media["poster_path"]
            }
        contenidos.append(current_contenido) 

    return contenidos




