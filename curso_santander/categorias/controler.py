from fastapi import APIRouter, Body, status, HTTPException
from datetime import datetime, timezone
from pydantic import UUID4
from curso_santander.categorias.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from curso_santander.categorias.models import CategoriaModel

from curso_santander.contrib.dependencies import DatabaseDependency

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter()

async def _get_categoria_by_id(id: UUID4, db_session: DatabaseDependency) -> CategoriaModel:
    """
    Busca uma categoria pelo ID. Se não encontrar, lança HTTPException 404.
    """
    categoria = (
        (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    )

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id: {id}")
    return categoria


@router.post(
    "/",
    summary="Criar uma nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    try:
        categoria_model = CategoriaModel(**categoria_in.model_dump())
        categoria_model.created_at = datetime.now(timezone.utc)
        db_session.add(categoria_model)
        await db_session.commit()
        await db_session.refresh(categoria_model)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe uma categoria com o nome: {categoria_in.nome}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco",
        )

    return categoria_model


@router.get(
    "/",
    summary="Consultar todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CategoriaOut],
)
async def get_all(db_session: DatabaseDependency) -> LimitOffsetPage[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel).order_by(CategoriaModel.nome))).scalars().all()
    return paginate(categorias)


@router.get(
    "/{id}",
    summary="Consultar uma categoria pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    return await _get_categoria_by_id(id, db_session)


@router.patch(
    "/{id}",
    summary="Editar uma categoria pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, cat_up: CategoriaUpdate = Body(...)) -> CategoriaOut:
    categoria = await _get_categoria_by_id(id, db_session)
    cat_update_data = cat_up.model_dump(exclude_unset=True)
    for key, value in cat_update_data.items():
        setattr(categoria, key, value)

    await db_session.commit()
    await db_session.refresh(categoria)

    return categoria


@router.delete("/{id}", summary="Deletar uma categoria pelo id", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    categoria = await _get_categoria_by_id(id, db_session)
    await db_session.delete(categoria)
    await db_session.commit()
