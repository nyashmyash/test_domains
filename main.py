from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

import asyncio


DATABASE_URL = "sqlite+aiosqlite:///domains.db"

from sqlalchemy import Column, Integer, Text


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Domains(Base):
    __tablename__ = "domains"
    name = Column(Text)
    project_id = Column(Integer, autoincrement=True, primary_key=True, index=True)


class Rules(Base):
    __tablename__ = "rules"
    regexp = Column(Text)
    project_id = Column(Integer, autoincrement=True, primary_key=True, index=True)


async def get_domains(async_session: async_sessionmaker[AsyncSession]) -> list:
    async with async_session() as session:
        result = await session.execute(select(Domains))
        data = result.scalars().all()
        for d in data:
            r = Rules()
            cnt_domains = len(d.name.split('.'))
            r.project_id = d.project_id
            reg = "//\w+\." * (cnt_domains - 1)
            r.regexp = "(" + reg + "\w+$" + ")|(" + reg + "/)"
            session.add(r)
        await session.commit()


async def main():
    await get_domains(async_session)

if __name__ == "__main__":
    asyncio.run(main())

#test
# import re
# s = "https://fff.fff.fggg.gggg"
# print(re.findall(r"(//\w+\.\w+\.\w+\.\w+$)|(//\w+\.\w+\.\w+\.\w+/)", s))
