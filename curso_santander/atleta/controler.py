from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4
from sqlalchemy.orm import selectinload
from curso_santander.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaOutResumido
from curso_santander.atleta.models import AtletaModel

from curso_santander.categorias.models import CategoriaModel
from curso_santander.centro_treinamento.models import CentroTreinamentoModel
from curso_santander.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter()


async def _get_atleta_by_id(id: UUID4, db_session: DatabaseDependency) -> AtletaModel:
    """
    Busca um atleta pelo ID. Se não encontrar, lança HTTPException 404.
    """
    atleta = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no id: {id}")
    return atleta


@router.post("/", summary="Criar um novo atleta.", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)) -> AtletaOut:

    categoria = (
        (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"A categoria {atleta_in.categoria.nome} não foi encontrada"
        )

    centro_treinamento = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome)))
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {atleta_in.centro_treinamento.nome} não foi encontrada",
        )

    try:
        atleta_model = AtletaModel(**atleta_in.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.id
        atleta_model.centro_treinamento_id = centro_treinamento.id

        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco",
        )

    return atleta_model


@router.get(
    "/",
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaOutResumido],
)
async def get_all(
    db_session: DatabaseDependency,
    nome: str | None = Query(default=None, description="Nome do atleta"),
    cpf: str | None = Query(default=None, description="CPF do atleta"),
) -> LimitOffsetPage[AtletaOutResumido]:

    query = (
        select(AtletaModel).options(selectinload(AtletaModel.categoria), selectinload(AtletaModel.centro_treinamento)).order_by(AtletaModel.nome)
    )

    if nome:
        query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    result = await db_session.execute(query)
    atletas = result.scalars().all()

    return paginate(atletas)


@router.get(
    "/{id}",
    summary="Consultar um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    return await _get_atleta_by_id(id, db_session)


@router.patch(
    "/{id}",
    summary="Editar um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta = await _get_atleta_by_id(id, db_session)
    atleta_update = atleta_up.model_dump(exclude_unset=True)

    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete("/{id}", summary="Deletar um atleta pelo id", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta = await _get_atleta_by_id(id, db_session)
    await db_session.delete(atleta)
    await db_session.commit()
