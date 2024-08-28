import asyncio

from fastapi.encoders import jsonable_encoder

from app.util import date as Dt
from app.service.response.result import ResultAPI
from app.service.middleware.audit.audit import Audit
from app.service.middleware.auth.auth import Auth
from app.service.middleware.notification.notify import Notify

from starlette.responses import Response


def audit(func):
    async def wrapper(*args, **kwargs):
        # user = kwargs.get("user", None)
        # id_user = user.id if user else None

        id_login = kwargs.get("id_login", None)

        content = kwargs.get("content", None)
        request = kwargs.get("request", None)

        # Se toma medida del tiempo antes de ejecutar la funcion
        timestamp_init = Dt.get_str_timestamp()
        # print("Me meto en la funcion", timestamp_init)
        response = None

        try:
            response = await func(*args, **kwargs)
            return response

        finally:
            timestamp_end = Dt.get_str_timestamp()

            result = None

            if response:
                if isinstance(response, str):
                    result = jsonable_encoder(ResultAPI(code=response))

                elif not isinstance(response, Response):
                    data = jsonable_encoder(response)
                    result = data.get("result", None)

            else:
                result = jsonable_encoder(ResultAPI(error=True))

            # Se toma medida del tiempo al finalizar la funcion
            asyncio.create_task(
                Audit.save_audit(
                    request, id_login, content, result, timestamp_init, timestamp_end
                )
            )

    return wrapper


def notify(func):
    async def wrapper(self, user, *args, **kwargs):
        result_code, seed_notification = await func(self, user, *args, **kwargs)

        asyncio.create_task(
            Notify.notify_event(
                self.id_funtionality, result_code, user, seed_notification
            )
        )
        return result_code, seed_notification

    return wrapper


def auth(func):
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token", None)
        segment_1 = kwargs.get("segment_1", None)
        segment_2 = kwargs.get("segment_2", None)
        segment_3 = kwargs.get("segment_3", None)
        segment_4 = kwargs.get("segment_4", None)
        content = kwargs.get("content", None)

        request = kwargs.get("request", None)

        funtionality, id_login, user = await Auth().check_authoritation(
            token, segment_1, segment_2, segment_3, segment_4, content, request
        )  # En caso de no realizarse la autorizacion check_authoritation crea una excepcion que termina con la request

        return await func(
            *args, **kwargs, id_login=id_login, user=user, funtionality=funtionality
        )

    return wrapper


def debug(func):
    async def wrapper(*args, **kwargs):

        print("=" * 60)
        print(f"                        DEBUG: {func.__name__}\n")
        for key, value in kwargs.items():
            print(f"{key}: {value}\n")
        try:
            response = await func(*args, **kwargs)
            print(f"\nResponse: {response}\n")
            return response
        finally:
            print("=" * 60)

    return wrapper


# async def audit(func):
#     async def wrapper(*args, **kwargs):
#         id_user = kwargs.get("id_user", None)

#         id_user = None

#         # Ejecutar la auditoría en un hilo paralelo
#         audit_thread = threading.Thread(target=audit.audit_request)
#         audit_thread.start()

#         # Ejecutar la función original y obtener la respuesta
#         response_data = func(*args, **kwargs)

#         # Procesar la respuesta
#         audit.set_response_data(response_data)

#         # Devolver la respuesta sin esperar a que la auditoría haya terminado
#         return response_data

#     return wrapper
