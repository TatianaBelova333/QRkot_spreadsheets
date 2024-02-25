from aiogoogle import Aiogoogle
from app.schemas.charity_project import CharyProjectReport
from app.services.google_api import spreadsheets_create, set_user_permissions, spreadsheets_update_value
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud import charity_project_crud

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

) -> dict[str, str]:
    projects = await charity_project_crud.get_project_by_completion_rate(
        session=session,
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id,
                                    projects,
                                    wrapper_services)

    return {
        'link_to_report': ('https://docs.google.com/spreadsheets/d/'
                           + spreadsheet_id)
        }
