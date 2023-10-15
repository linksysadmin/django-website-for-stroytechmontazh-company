from sqlalchemy import create_engine, func, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

from config import SQLALCHEMY_DATABASE_URI

Model = declarative_base(name='Model')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(engine, autoflush=False, autocommit=False)
session = Session()


class ServiceType(Model):
    __tablename__ = 'flushing_typeflushingservice'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    slug = Column(String(255), unique=True)


class Service(Model):
    __tablename__ = 'flushing_flushingservice'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    slug = Column(String(255), unique=True)
    service_type_id = Column(Integer, ForeignKey('flushing_typeflushingservice.id'))
    service_type = relationship(ServiceType)
    description = Column(Text)
    price = Column(Float(precision=2))
    image = Column(String)
    is_published = Column(Boolean, default=True)


class Feedback(Model):
    __tablename__ = 'flushing_feedback'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(16), nullable=False)
    time_create = Column(DateTime, nullable=False, server_default=func.now())
    time_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
