from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
