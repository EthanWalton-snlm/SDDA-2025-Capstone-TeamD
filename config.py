from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("LOCAL_DATABASE_URL")
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False
