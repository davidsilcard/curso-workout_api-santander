from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from datetime import datetime, timezone
from curso_santander.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut, CentroTreinamentoUpdate
from curso_santander.centro_treinamento.models import CentroTreinamentoModel

from curso_santander.contrib.dependencies import DatabaseDependency

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter()


async def _get_centro_treinamento_by_id(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoModel:
    """
    Busca um centro de treinamento pelo ID. Se não encontrar, lança HTTPException 404.
    """
    centro_treinamento = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado no id: {id}"
        )
    return centro_treinamento

@router.post(
    "/",
    summary="Criar um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    try:
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_in.model_dump())
        centro_treinamento_model.created_at = datetime.now(timezone.utc)
        db_session.add(centro_treinamento_model)
        await db_session.commit()
        await db_session.refresh(centro_treinamento_model)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um centro de treinamento com o nome: {centro_treinamento_in.nome}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco",
        )
    return centro_treinamento_model


@router.get(
    "/",
    summary="Consultar todos os centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CentroTreinamentoOut],
)
async def get_all(db_session: DatabaseDependency) -> LimitOffsetPage[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (
        (await db_session.execute(select(CentroTreinamentoModel).order_by(CentroTreinamentoModel.nome))).scalars().all()
    )
    return paginate(centros_treinamento)


@router.get(
    "/{id}",
    summary="Consultar um centro de treinamento pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    return await _get_centro_treinamento_by_id(id, db_session)


@router.patch(
    "/{id}",
    summary="Editar um centro de treinamento pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, ct_up: CentroTreinamentoUpdate = Body(...)) -> CentroTreinamentoOut:
    centro_treinamento = await _get_centro_treinamento_by_id(id, db_session)

    ct_update = ct_up.model_dump(exclude_unset=True)
    for key, value in ct_update.items():
        setattr(centro_treinamento, key, value)

    await db_session.commit()
    await db_session.refresh(centro_treinamento)

    return centro_treinamento


@router.delete("/{id}", summary="Deletar um centro de treinamento pelo id", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    centro_treinamento = await _get_centro_treinamento_by_id(id, db_session)
    await db_session.delete(centro_treinamento)
    await db_session.commit()
