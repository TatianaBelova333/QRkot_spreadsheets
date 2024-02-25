from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from sqlalchemy.engine.row import Row

from app.core.config import settings
from app.core.constants import (COLUMN_COUNT, FIRST_SHEET_TITLE,
                                GOOGLE_SHEETS_NAME,
                                GOOGLE_SHEET_COLUMNS,
                                GOOGLE_SHEETS_LOCALE,
                                GOOGLE_SHEET_RANGE,
                                GOOGLE_SHEET_TITLE,
                                ROW_COUNT)

REPORT_NAME = GOOGLE_SHEETS_NAME.format(now=datetime.now())


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Create a new Google sheet document and return the document id.

    """

    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {'title': REPORT_NAME,
                       'locale': GOOGLE_SHEETS_LOCALE},
        'sheets': [{'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': FIRST_SHEET_TITLE,
            'gridProperties': {'rowCount': ROW_COUNT,
                               'columnCount': COLUMN_COUNT}
        }
        }]
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
    """Set writer permission to access Google sheets documents."""
    writer_permission = {'type': 'user',
                         'role': 'writer',
                         'emailAddress': settings.email}

    service = await wrapper_services.discover('drive', 'v3')

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=writer_permission,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list[Row],
        wrapper_services: Aiogoogle,
) -> None:
    """
    Fill out the specific Google sheet document
    with the list of closed charity projects ordered by the period of closure
    in ascending order limited by the ROW_COUNT value.

    """
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        REPORT_NAME.split(),
        GOOGLE_SHEET_TITLE,
        GOOGLE_SHEET_COLUMNS,
    ]

    for project in charity_projects:

        new_row = [
            project.name,
            str(timedelta(seconds=project.period_in_sec)),
            project.description,
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values[:ROW_COUNT]
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=GOOGLE_SHEET_RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
