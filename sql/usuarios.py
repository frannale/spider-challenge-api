from sqlalchemy.orm import Session
from . import models
from .schemas import usuarios as UsuarioSchema
from security import utils

import os

from dotenv import dotenv_values
BASEDIR = os.path.abspath(os.path.dirname("./"))
config = dotenv_values(os.path.join(BASEDIR, ".env"))

def get_usuario_by_id(db: Session, id_usuario: int):
    return db.query(models.Usuario).filter(models.Usuario.id == id_usuario).first()

def delete_usuario_by_id(db: Session, id_usuario: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id_usuario).first()
    db.delete(usuario)
    db.commit()
    return True

def crear_usuario(db: Session, usuario: UsuarioSchema.UsuarioCreate):
    nuevo_usuario = models.Usuario(
        username= usuario.username,
        password= utils.get_hash_password(usuario.password) 
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def modificar_usuario(db: Session, id_usuario: int ,usuario: UsuarioSchema.UsuarioCreate):

    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == id_usuario).first()
    usuario_db.username = usuario.username
    if(usuario.password != ""):
        usuario_db.password= utils.get_hash_password(usuario.password)
    
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def get_usuario_by_nombre(db: Session, username: str):
    usuario = (
        db.query(models.Usuario).filter(models.Usuario.username == username).first()
    )
    if usuario != None:
        return UsuarioSchema.UsuarioEnDB(
            id=usuario.id, username=usuario.username, hashed_password=usuario.password
        )