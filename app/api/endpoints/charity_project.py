from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_for_name_duplicate,
                                check_charity_project_is_opened,
                                check_charity_project_not_partially_invested,
                                check_proj_new_full_amnt_more_than_invst_amnt)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import (CharityProjectDB, CharityProjectCreate,
                         CharityProjectUpdate)
from app.services.investment import invest


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_list(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_for_name_duplicate(name=charity_project.name, session=session)

    new_charity_project: CharityProject = await charity_project_crud.create(
        charity_project,
        session,
    )

    new_charity_project: CharityProject = await invest(
        new_invest_item=new_charity_project,
        item_to_check='donation',
        session=session,
    )

    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)

    await check_charity_project_not_partially_invested(charity_project)

    charity_project = await charity_project_crud.remove(
        charity_project, session
    )

    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):

    charity_project = await check_charity_project_exists(project_id, session)

    await check_charity_project_is_opened(charity_project)

    await check_for_name_duplicate(name=obj_in.name, session=session)

    await check_proj_new_full_amnt_more_than_invst_amnt(
        current_project=charity_project,
        updated_project=obj_in,
    )

    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=obj_in,
        session=session,
    )
    return charity_project
