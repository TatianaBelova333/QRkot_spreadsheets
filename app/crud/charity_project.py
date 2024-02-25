from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def check_name_duplicates(
            self,
            project_name: Optional[str],
            session: AsyncSession,
    ) -> Optional[bool]:
        """
        Return True if the project name (case-insensitive) is already in db.
        False, otherwise.

        """
        project_name = project_name.lower() if project_name else project_name

        exists_criteria = (
            select(CharityProject).where(
                func.lower(CharityProject.name) == project_name
            ).exists()
        )

        duplicate_name_exists = await session.scalar(
            select(True).where(exists_criteria)
        )

        return bool(duplicate_name_exists)

    async def remove(
            self,
            db_obj: CharityProject,
            session: AsyncSession,
    ):
        """
        Remove the db_obj from db.

        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_project_by_completion_rate(
            self,
            session: AsyncSession,

    ) -> list[tuple[str, str, int]]:
        money_raise_period = (func.extract('epoch', self.model.close_date) -
                              func.extract('epoch', self.model.create_date))
        closed_projects = await session.execute(
            select(self.model.name,
                   self.model.description,
                   money_raise_period.label('period_in_sec')).where(
                self.model.fully_invested.is_(True)
            ).order_by(money_raise_period)
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
