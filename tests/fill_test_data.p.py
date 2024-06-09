import asyncio

from src.dependencies import get_async_session
from tests.dumps.dumps_account import create_test_users


async def main():
    async for db in get_async_session():
        await create_test_users(db)
    # fill another data here

asyncio.run(main())
