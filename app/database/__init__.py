from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.database.models import Response, Website

