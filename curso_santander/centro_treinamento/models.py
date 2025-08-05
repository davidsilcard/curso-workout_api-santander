from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from curso_santander.contrib.models import BaseModel


class CentroTreinamentoModel(BaseModel):
    __tablename__ = "centros_treinamento"

    # pk_id: Mapped[int] = mapped_column(Integer, primary_key=True) # Removido, o ID agora vem do BaseModel
    nome: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    atletas: Mapped[list['AtletaModel']] = relationship(back_populates='centro_treinamento')