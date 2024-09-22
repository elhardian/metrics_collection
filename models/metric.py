from uuid import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class Metric(Base):
    __tablename__ = 'users'
    id: UUID
    function: Column()