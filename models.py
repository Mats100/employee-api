from sqlalchemy import Column, INTEGER, String
from database import Base


class Employees(Base):
    __tablename__ = 'employee'
    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String)
    profession = Column(String)
