from typing import Annotated, Optional

from pydantic import Field
from curso_santander.contrib.schemas import BaseSchema, OutMixin


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Scale", max_length=50)]

class CategoriaOut(CategoriaIn, OutMixin):
    pass


class CategoriaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome da categoria", example="Scale", max_length=50)]