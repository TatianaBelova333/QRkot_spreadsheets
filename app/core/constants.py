from app.core.config import settings

NAME_MAX_VAL = 100
NAME_MIN_VAL = 1
TOKEN_LIFETIME = 3600
PASSWORD_LENGTH = 3
GOOGLE_SHEET_MAIN_URL = 'https://docs.google.com/spreadsheets/d/'
REPORT_DATE_FORMAT = "%Y/%m/%d %H:%M"
GOOGLE_SHEETS_NAME = 'Отчёт на {now:{date_format}}'
GOOGLE_SHEETS_LOCALE = 'ru_RU'
COLUMN_COUNT = 3
ROW_COUNT = 100
GOOGLE_SHEET_RANGE = f'A1:C{ROW_COUNT}'
GOOGLE_SHEET_TITLE = 'Отчёт от'
GOOGLE_SHEET_SUBTITLE = ['Топ проектов по скорости закрытия']
GOOGLE_SHEET_COLUMNS = ['Название проекта', 'Время сбора', 'Описание']
FIRST_SHEET_TITLE = 'Закрыты проекты'
GOOGLE_DRIVE_PERMISSION = {'type': 'user',
                           'role': 'writer',
                           'emailAddress': settings.email}
FIRST_SHEET_PROPERTIES = {'properties': {
    'sheetType': 'GRID',
    'sheetId': 0,
    'title': FIRST_SHEET_TITLE,
    'gridProperties': {
        'rowCount': ROW_COUNT,
        'columnCount': COLUMN_COUNT
    }
}}
GOOGLE_SHEET_DIMENSION = 'ROWS'
SHEET_INPUT_OPTION = 'USER_ENTERED'
