from sqlalchemy import Column, String, Float, Boolean
from models.base import BaseDatabaseModel

class Metric(BaseDatabaseModel):
    __tablename__ = 'metrics'

    function_name = Column(String, default="")
    execution_time = Column(Float, default="")
    is_error = Column(Boolean, default="")