from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[int] = Field(gt=0)
    create_date: Optional[datetime]


class UserDonationDB(DonationBase):
    """Donation schema for the current user's donations."""
    id: int

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    """Donation schema for the superuser's donations."""
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime]
    user_id: int

    class Config:
        orm_mode = True


class DonationCreate(BaseModel):
    """Donation schema for creating a donation."""
    comment: Optional[str]
    full_amount: int = Field(gt=0)

    class Config:
        extra = Extra.forbid
