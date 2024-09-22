from sqlalchemy import Column, String, BigInteger
from models.base import BaseDatabaseModel

class Metric(BaseDatabaseModel):
    __tablename__ = 'metric'

    function_name = Column(String, default="")
    execution_time = Column(BigInteger, default="")