from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from curso_santander.contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = "atletas"
 
    # pk_id: Mapped[int] = mapped_column(Integer, primary_key=True) # Removido, o ID agora vem do BaseModel
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    categoria: Mapped['CategoriaModel'] = relationship(back_populates='atletas')
    categoria_id: Mapped[UUID] = mapped_column(ForeignKey('categorias.id'), nullable=False)
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates='atletas')
    centro_treinamento_id: Mapped[UUID] = mapped_column(ForeignKey('centros_treinamento.id'), nullable=False)
