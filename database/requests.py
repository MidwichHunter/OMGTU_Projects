from database.models import async_session
from database.models import User, Category, Marathone
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_Maraphone(Marathone_choose: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.Marathone_choose == None))
        user.Marathone_choose = Marathone_choose
        await session.commit()

        if not user:
            session.add(User(Marathone_choose=Marathone_choose))
            await session.commit()


async def set_FIO(FIO: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.FIO == None))
        user.FIO = FIO
        await session.commit()

        if not user:
            session.add(User(FIO = FIO))
            await session.commit()


async def delete_Maraphone() -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.Marathone_choose != None))
        user.Marathone_choose = None
        await session.commit()




async def delete_FIO() -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.FIO != None))
        user.FIO = None
        await session.commit()



async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Marathone).where(Marathone.category == category_id))


async def get_Marathone(marathone_id):
    async with async_session() as session:
        return await session.scalar(select(Marathone).where(Marathone.id == marathone_id))

async def get_Data():
    async with async_session() as session:
        if User.Marathone_choose is None:
            return 0
        else:
            return await session.scalar(select(User.Marathone_choose))

async def get_user():
    async with async_session() as session:
        return await session.scalar(select(User.id))