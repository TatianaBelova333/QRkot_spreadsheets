from sqlalchemy import Column, String, Text

from app.core.constants import NAME_MAX_VAL
from app.core.db import Base
from app.models import InvestmentMixin


class CharityProject(InvestmentMixin, Base):
    name = Column(String(NAME_MAX_VAL), unique=True, nullable=False)
    description = Column(Text, nullable=False)
