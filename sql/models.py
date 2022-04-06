from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(40), unique=True)
    password = Column(String(800))
    favoritos = relationship( "Favorito", back_populates="usuario")

class Favorito(Base):
    __tablename__ = "favorita"

    id = Column(Integer, primary_key=True, index=True)
    id_pelicula = Column(Integer)
    fecha = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", back_populates="favoritos")
