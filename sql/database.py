from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import os

BASEDIR = os.path.abspath(os.path.dirname("./"))

config = dotenv_values(os.path.join(BASEDIR, ".env"))

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        config["DB_USER"], config["DB_PASS"], config["DB_HOST"], config["DB_NAME"]
    )
 )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
