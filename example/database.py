from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

# Cria a classe Base do SQLAlchemy (na versão 2.x)
Base = declarative_base()

class Pessoas(Base):
    """Define a tabela no banco de dados."""
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    idade = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)