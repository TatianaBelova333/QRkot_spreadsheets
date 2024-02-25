from abc import ABCMeta
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class InvestmentMixin(object):
    __metaclass__ = ABCMeta

    full_amount = Column(
        Integer,
        nullable=False,
    )
    invested_amount = Column(
        Integer,
        nullable=False,
        default=0,
    )
    fully_invested = Column(
        Boolean,
        nullable=False,
        default=False,
    )
    create_date = Column(
        DateTime,
        nullable=False,
        index=True,
        default=datetime.now,
    )
    close_date = Column(
        DateTime,
        index=True,
        default=None,
    )
