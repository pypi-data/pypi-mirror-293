import pytest

from app.util import asynchrony as As
import time
import asyncio


@pytest.mark.asyncio
async def test_async_execute():
    scheduled_task = False

    # Función de ejemplo para usar en los casos de prueba
    def addition(a, b):
        return a + b

    def delay_sync_func():
        time.sleep(1)  # Simular una operación que toma 1 segundo
        return "Función con retraso ejecutada"

    def check_async_task():
        nonlocal scheduled_task
        for task in asyncio.all_tasks():
            if task.get_name() == "async_execute":
                scheduled_task = True

    # Caso de prueba 1: Verificar que la función devuelve el resultado correcto para una suma
    result_add = await As.async_execute(addition, 2, 3)
    assert result_add == 5

    with pytest.raises(TypeError):
        await As.async_execute(addition, "a", 3)

    asyncio.create_task(As.async_execute(
        delay_sync_func), name="async_execute")
    await asyncio.sleep(0.1)
    check_async_task()
    assert scheduled_task == True
