import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('.env')
conexao_local = config.get('base_dados_local', 'conexao')
engine = create_engine(conexao_local)

Base = declarative_base()

class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)
    identificador = Column(String(250), nullable=False)

class VazaoAgua(Base):
    __tablename__ = 'vazaoagua'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True), server_default=func.now())
    sincronizado = Column(Integer, default=0)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)
    
class FluxoAgua(Base):
    __tablename__ = 'fluxoagua'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True), server_default=func.now())
    sincronizado = Column(Integer, default=0)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

class Temperatura(Base):
    __tablename__ = 'temperatura'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True), server_default=func.now())
    sincronizado = Column(Integer, default=0)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

class Umidade(Base):
    __tablename__ = 'umidade'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True), server_default=func.now())
    sincronizado = Column(Integer, default=0)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    mensagem = Column(String(1000), nullable=False)
    datahora = Column(DateTime(timezone=True), server_default=func.now())
    sincronizado = Column(Integer, default=0)
    sensor_id = Column(Integer, default=0)

engine = create_engine(conexao_local)

Base.metadata.create_all(engine)
