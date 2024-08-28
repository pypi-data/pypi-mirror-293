import asyncio
from concurrent.futures import ThreadPoolExecutor


# Convierte una funcion sincrona en asincrona
async def async_execute(callback, *args):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=1) as executor:
        return await loop.run_in_executor(executor, lambda: callback(*args))
