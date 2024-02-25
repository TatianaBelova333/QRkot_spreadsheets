from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.core.constants import NAME_MAX_VAL, NAME_MIN_VAL


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=NAME_MAX_VAL,
    )
    description: Optional[str]
    full_amount: int = Field(None, gt=0)

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = NAME_MIN_VAL


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: Optional[datetime]
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        max_length=NAME_MAX_VAL,
    )
    description: str
    full_amount: int = Field(gt=0)

    class Config:
        extra = Extra.forbid
        min_anystr_length = NAME_MIN_VAL
        anystr_strip_whitespace = True


class CharityProjectUpdate(CharityProjectBase):

    @validator('name', 'description')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя не может быть None')
        return value

    class Config:
        extra = Extra.forbid
