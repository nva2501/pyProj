from fastapi import Request
import asyncio

async def disconnect_checker(request: Request):
    while True:
        await asyncio.sleep(0.2)
        if await request.is_disconnected():
            raise asyncio.CancelledError()
