from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from sqlalchemy.engine.row import Row

from app.core.constants import (FIRST_SHEET_PROPERTIES,
                                GOOGLE_DRIVE_PERMISSION,
                                GOOGLE_SHEET_DIMENSION,
                                GOOGLE_SHEETS_NAME,
                                GOOGLE_SHEET_COLUMNS,
                                GOOGLE_SHEETS_LOCALE,
                                GOOGLE_SHEET_RANGE,
                                GOOGLE_SHEET_TITLE,
                                ROW_COUNT,
                                SHEET_INPUT_OPTION)

REPORT_NAME = GOOGLE_SHEETS_NAME.format(now=datetime.now())

SPREADSHEET_BODY = {
    'properties': {'title': REPORT_NAME,
                   'locale': GOOGLE_SHEETS_LOCALE},
    'sheets': [FIRST_SHEET_PROPERTIES],
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Create a new Google sheet document and return the document id.

    """

    service = await wrapper_services.discover('sheets', 'v4')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']

    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Set writer permission to access Google sheets documents."""

    service = await wrapper_services.discover('drive', 'v3')

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=GOOGLE_DRIVE_PERMISSION,
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
        'majorDimension': GOOGLE_SHEET_DIMENSION,
        'values': table_values[:ROW_COUNT]
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=GOOGLE_SHEET_RANGE,
            valueInputOption=SHEET_INPUT_OPTION,
            json=update_body,
        )
    )
