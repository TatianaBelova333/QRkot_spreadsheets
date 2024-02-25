from datetime import datetime
from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject, Donation
from app.crud import charity_project_crud, donation_crud


async def close_investment_item(item):
    item.invested_amount = item.full_amount
    item.fully_invested = True
    item.close_date = datetime.now()
    return item


async def get_unclosed_investment_items(
        item: str,
        session: AsyncSession
) -> list[Union[Donation, CharityProject]]:

    item_crud = {
        'charity_project': charity_project_crud,
        'donation': donation_crud,
    }

    unclosed_items = await item_crud[item].get_not_fullyinvested_objs(
        session=session,
    )
    return unclosed_items


async def invest(
        new_invest_item: Union[CharityProject, Donation],
        item_to_check: str,
        session: AsyncSession = Depends(get_async_session),
) -> Union[CharityProject, Donation]:

    unclosed_invest_items = await get_unclosed_investment_items(
        item=item_to_check,
        session=session,
    )

    items_invested = []

    for item in unclosed_invest_items:
        if new_invest_item.fully_invested:
            break

        required_amount = (new_invest_item.full_amount -
                           new_invest_item.invested_amount)

        invt_avail_amt = item.full_amount - item.invested_amount

        if invt_avail_amt >= required_amount:
            await close_investment_item(new_invest_item)
            print(new_invest_item.fully_invested)
            if invt_avail_amt == required_amount:
                await close_investment_item(item)
            else:
                item.invested_amount += required_amount
        else:
            await close_investment_item(item)
            new_invest_item.invested_amount += invt_avail_amt

        items_invested.append(item)

    session.add(new_invest_item)
    session.add_all(items_invested)
    await session.commit()
    await session.refresh(new_invest_item)

    return new_invest_item
