import asyncio
import re

from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.util import request as Rq
from app.util import date as Dt
from app.service.middleware.audit.audit import Audit
from app.service.middleware.audit.payload import Payload
from app.service.middleware.auth.auth import Auth
from app.service.middleware.auth.conn import Conn, ConnKeys


class RequestRules:
    ALLOWED_METHODS = ["GET", "POST"]
    MALICIOUS_PATTERS = [
        r"<script>",
        r"<.*>",
        r"(SELECT|INSERT|UPDATE|DELETE|OR|AND)",
        r";",
        r"\|",
        r"`",
        r"\$\(.*?\)",
        r"cat|ls|pwd|cd|rm|mv|cp|mkdir|touch|echo|wget|curl",
        r"base64_decode|eval|system|exec|passthru|shell_exec|popen|proc_open",
        r"/bin/|/etc/passwd|/etc/shadow|/dev/null",
        r"\.\.",
        r"/\w+/(passwd|shadow|bash_history)",
        r"(\d+\.\d+\.\d+\.\d+)",  # Detectar direcciones IP
        # Detectar rangos de direcciones IP
        r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})",
        r"(localhost|127\.0\.0\.1)",  # Detectar localhost
        r"<!--.*?-->",  # Comentarios HTML
        # Acceso a objetos del navegador
        r"(document\.|window\.|navigator\.|cookie\.|localStorage\.|sessionStorage\.)",
        r"\\.\\.",  # Traversal de directorios
        r"\\/",  # Traversal de directorios
        r"/\.\./",  # Traversal de directorios
        r"/\.",  # Traversal de directorios
        # Directorios de sistema comunes
        r"( /bin | /etc | /dev | /usr | /tmp | /var | /proc | /opt | /home | /root | /sys | /sbin | /lib )",
    ]


class SecurityMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, secure_headers=None):
        super().__init__(app)
        self.secure_headers = secure_headers

    async def dispatch(self, request, call_next):
        id_conn = await Conn.get_connection(request)
        if id_conn is not None:
            # Se captura el timestamp en el momento que entra la solicitud
            timestamp = Dt.get_str_timestamp()
            await self.audit_request_not_logged(request, id_conn, timestamp)

            if await self._allowed_http_method(
                request, id_conn
            ) and not await self._payload_in_request(request, id_conn):

                response = await call_next(request)
                self.secure_headers.framework.fastapi(response)
                return response
            else:
                return Response(
                    status_code=401, content="Request audited and will be reported"
                )

        return Response(status_code=401)

    ###########################################################################################
    #################### Auditoria de las request no loggeadas / sin token ####################
    ###########################################################################################
    async def audit_request_not_logged(self, request, id_conn, timestamp):
        try:
            token = Rq.get_authorization_token(request)

            # Se comprueba si hay token en la cookie
            if not token:
                token = Rq.get_token_from_cookie(request)

            is_valid = Auth().is_valid_token(token)

            if is_valid is False:  # Es un token alterado
                await Conn.block_conn(request, id_conn, reason=ConnKeys.ALTER_TOKEN)
                asyncio.create_task(
                    Audit.audit_request_not_logged(request, id_conn, timestamp)
                )
            if is_valid is None:  # No lleva token, se audita
                asyncio.create_task(
                    Audit.audit_request_not_logged(request, id_conn, timestamp)
                )
                asyncio.create_task(Conn.analyze_request_not_logged(request, id_conn))

        except Exception as e:
            print("ERROR: Auth Conn -> audit_request_not_logged: " + str(e))

    ###########################################################################################
    ######### Metodos de verificacion de la request en el mismo momento que se recibe #########
    ###########################################################################################
    async def _allowed_http_method(self, request, id_conn) -> bool:
        try:
            if Rq.get_method(request) in RequestRules.ALLOWED_METHODS:
                return True

            # Se audita el payload
            asyncio.create_task(Payload.audit(id_conn, str(request.method)))
            await Conn.block_conn(request, id_conn, reason=ConnKeys.BAD_METHOD)
            return False

        except NameError or AttributeError as e:
            print(
                "ERROR: Middleware RequestMiddleware -> allowed_http_method: " + str(e)
            )

        return False

    async def _payload_in_request(self, request, id_conn) -> bool:
        try:
            # Obtener el método de solicitud HTTP (GET, POST, etc.)
            method = Rq.get_method(request)
            payload = None

            # Obtener el payload de la solicitud si existe
            if method == "GET":
                payload = Rq.get_params(request)

            if payload:
                for pattern in RequestRules.MALICIOUS_PATTERS:
                    if re.search(pattern, payload):
                        asyncio.create_task(Payload.audit(id_conn, payload))
                        await Conn.block_conn(request, id_conn, reason=ConnKeys.HACKER)
                        return True

            return False
        except NameError or AttributeError as e:
            print(
                "ERROR: Middleware RequestMiddleware -> payload_in_request: " + str(e)
            )

        return False
