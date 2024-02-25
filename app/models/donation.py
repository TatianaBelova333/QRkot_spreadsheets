from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models import InvestmentMixin


class Donation(InvestmentMixin, Base):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='donations')
