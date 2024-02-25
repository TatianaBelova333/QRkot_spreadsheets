from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_for_name_duplicate(
        name: Optional[str],
        session: AsyncSession,
) -> None:
    """
    Check for name duplicates. Raises a 400 Bad Request HTTPException if
    the name already exists in db.

    """
    duplicate_name_exists = await charity_project_crud.check_name_duplicates(
        project_name=name,
        session=session,
    )

    if duplicate_name_exists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Return a CharityProject instance with with the provided charity_project_id.
    Raise a 404 Not Found HTTPException, otherwise.

    """
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id,
        session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='The project does not exist!',
        )
    return charity_project


async def check_charity_project_is_opened(
    charity_project: CharityProject,
) -> None:
    """
    Raises a 400 Bad Request HTTPException if the close_date field
    of CharityProject is not None.

    """
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_charity_project_not_partially_invested(
    charity_project: CharityProject,
) -> None:
    """
    Raises a 400 Bad Request HTTPException if the invested field
    of CharityProject instance is above 0.

    """
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(('В проект были внесены средства, '
                    'не подлежит удалению!')),
        )


async def check_proj_new_full_amnt_more_than_invst_amnt(
    current_project: CharityProject,
    updated_project: CharityProjectUpdate,
) -> None:
    """
    Raise a 400 Bad Request HTTPException if the full amount
    of the existing project is lower than the new full amount value.

    """
    new_full_amount = updated_project.full_amount
    current_invested_amount = current_project.invested_amount

    if (new_full_amount is not None and
            new_full_amount < current_invested_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(('Нелья установить значение full_amount '
                     'меньше уже вложенной суммы.')),
        )
