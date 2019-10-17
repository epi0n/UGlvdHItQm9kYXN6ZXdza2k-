from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.database import Base


class Website(Base):
    __tablename__ = 'website'

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False)
    interval = Column(Integer)

    def __repr__(self):
        return f'<Id: {self.id}, URL: {self.url}>'


class Response(Base):
    __tablename__ = 'response'

    id = Column(Integer, autoincrement=True, primary_key=True)
    website_id = Column(Integer, ForeignKey('website.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    response = Column(String)
    duration = Column(Float)
    created_at = Column(Float)

    def __repr__(self):
        return f'<Id: {self.id}, Response: {self.response}>'
