from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from curso_santander.contrib.models import BaseModel


class CategoriaModel(BaseModel):
    __tablename__ = "categorias"

    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    atletas: Mapped[list["AtletaModel"]] = relationship(back_populates="categoria")
