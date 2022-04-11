from typing import List, Optional, Dict
from xmlrpc.client import Boolean

from pydantic import BaseModel, Field


class Contenido(BaseModel):

    nombre: str = Field(
        ...,
        title="Nombre descriptivo del contenido",
        example="La peli",
        max_length=100
    )
    tipo: str = Field(
        ...,
        title="Tipo del contenido",
        example="tv",
        max_length=50
    )
    poster: str = Field(
        ...,
        title="Imagen poster del contenido",
        example="/tFURJnWv5qW58x4OOrXt1GQEyr1.jpg",
        max_length=100
    )


""" <--- SCHEMAS DE RESPUESTA ---> """

class GetContenido(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    contenido: Contenido

class GetContenidos(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    contenidos: List[Contenido]


