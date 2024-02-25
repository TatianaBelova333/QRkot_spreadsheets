from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.schemas import CharyProjectReport

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:

    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}

    service = await wrapper_services.discover('drive', 'v3')

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list[CharyProjectReport],
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    row_count = len(table_values) + len(charity_projects)

    for project in charity_projects:

        new_row = [
            project.name,
            str(timedelta(seconds=project.period_in_sec)),
            project.description,
            ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{row_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
