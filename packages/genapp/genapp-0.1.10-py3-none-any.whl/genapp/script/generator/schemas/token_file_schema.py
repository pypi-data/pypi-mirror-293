import asyncio

from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi import status

from app.CRUD_KEY.DATABASE_NAME_KEY.API_USER_KEY_dao import CLASS_NAME_KEYDao
from app.MODEL_KEY.DATABASE_NAME_KEY.API_USER_KEY import CLASS_NAME_KEYModel
from app.util import string as St
from app.service.middleware.audit.login import Login, LoginStatus
from app.service.middleware.auth.auth import Auth
from app.service.middleware.auth.conn import Conn


class Token(Auth):

    MAX_ATTEMPS = 5

    async def login(self, form_data: OAuth2PasswordRequestForm, request: Request):
        username = form_data.username
        passwd = form_data.password

        id_conn = await Conn.get_connection(request)

        # Si no hay es que o esta bloqueada o se produce un error
        if id_conn is not None:

            user = CLASS_NAME_KEYModel(key=passwd, username=username)
            id_user = await CLASS_NAME_KEYDao().login(user)

            if id_user is not None:
                id_login = await Login.audit(
                    id_conn, LoginStatus.OK, request, username, passwd, id_user
                )
                access_token = await self._get_token(id_user, id_login, id_conn)
                return {"access_token": access_token, "token_type": "bearer"}

            else:  # Si el login falla se audita asincronamente
                await Login.audit(id_conn, LoginStatus.DENY, request, username, passwd)
                asyncio.create_task(Conn.analyze_login(request, id_conn))

        self.return_not_autenticated()

    async def login_web(self, form_data: OAuth2PasswordRequestForm, request: Request):
        email = form_data.username
        passwd = form_data.password

        id_conn = await Conn.get_connection(request)

        # Si no hay es que o esta bloqueada o se produce un error
        if id_conn is not None:

            user = CLASS_NAME_KEYModel(key=passwd, email=email)
            id_user = await CLASS_NAME_KEYDao().login(user)

            if id_user is not None:
                id_login = await Login.audit(
                    id_conn, LoginStatus.OK, request, email, passwd, id_user
                )

                response = JSONResponse(
                    content={"url": "/home"}, status_code=status.HTTP_200_OK
                )

                access_token = await self._get_token(id_user, id_login, id_conn)
                response.set_cookie(
                    key="access_token",
                    value=f"{access_token}",
                    httponly=True,
                    max_age=1800,  # 30 minutes
                    expires=1800,
                )

                return response

            return JSONResponse(
                content={"error": "Credenciales incorrectas"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        self.return_not_autenticated()

    async def _get_token(self, id_user, id_login, id_conn) -> str:
        if id_user is not None:
            while True:
                jti = St.random_string(10)
                if self._check_jti_cache(jti):
                    break

            access_token_jwt = self._create_token(jti)

            model = CLASS_NAME_KEYModel(id=id_user)
            scope = await CLASS_NAME_KEYDao().scope(model)

            token_data = self._format_cache_token_data(
                id_user, id_login, id_conn, self._new_session_time(), scope
            )

            if self._update_token_data(jti, token_data):

                return access_token_jwt
