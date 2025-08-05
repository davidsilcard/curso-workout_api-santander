from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from curso_santander.categorias.schemas import CategoriaIn
from curso_santander.centro_treinamento.schemas import CentroTreinamentoAtleta
from curso_santander.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do Atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do Atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do Atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do Atleta", example=75.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do Atleta", example=1.70)]
    sexo: Annotated[str, Field(description="Sexo do Atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass


class AtletaOutResumido(OutMixin, BaseSchema):
    nome: Annotated[str, Field(description="Nome do Atleta", example="João", max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do Atleta", example="João", max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do Atleta", example=25)]
