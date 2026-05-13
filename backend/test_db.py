import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

async def test():
    url = os.getenv("DATABASE_URL")
    print(f"Testing connection to: {url}")
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("Database connection: SUCCESS", result.scalar())
    await engine.dispose()

asyncio.run(test())
