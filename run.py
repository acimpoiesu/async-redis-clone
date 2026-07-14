import asyncio
from app.server import start_server 
from app.store import db

async def main():
    asyncio.create_task(db.eviction_loop())
    await start_server()
    
if __name__ == "__main__":
    asyncio.run(main())