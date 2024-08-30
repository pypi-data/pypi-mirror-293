import os
from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.CRUD_KEY.DATABASE_NAME_KEY.API_USER_KEY_dao import CLASS_NAME_KEYDao
from app.MODEL_KEY.DATABASE_NAME_KEY.API_USER_KEY import CLASS_NAME_KEYModel

from app.service import cache as Cache
from app.service.controller import Controller
from app.service.middleware.audit.login import Login
from app.service.middleware.auth.conn import Conn

from app.util import json as Js
from app.util import request as Rq


class Auth(Controller):
    # Tiempo maximo de inactividad para una sesion
    TIME_SESSION_EXPIRES = 10

    NOT_AUTH_NEEDED = 0
    AUTH_NEEDED = 1

    # Claves del contenido del token
    EXP = "exp"
    JTI = "jti"
    IAT = "iat"

    # Algoritmo de cifrado
    ALGORITHM = "HS256"

    def __init__(self):
        self.SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")

    # Devuelve id_user si el token es valido para acceder a una funcionalidad
    # en caso contrario devolvera el codigo de error pertinente
    async def check_authoritation(
        self,
        token,
        segment_1,
        segment_2=None,
        segment_3=None,
        segment_4=None,
        content=None,
        request=None,
    ):
        id_funtionality = None
        is_auth_needed = None
        id_login = None
        user = None

        # Se comprueba si hay token en la cookie
        if not token:
            token = Rq.get_token_from_cookie(request)

        # Se obtiene el id de funcionalidad
        funtionality = Cache.get_id_funtionality(
            segment_1, segment_2=segment_2, segment_3=segment_3, segment_4=segment_4
        )

        if funtionality is not None:
            id_funtionality = funtionality.id
            is_auth_needed = funtionality.auth

        if is_auth_needed == self.AUTH_NEEDED:
            if token != None:
                id_login, id_user, scope = await self._validate_token(token, request)

                if id_user != None:
                    if id_funtionality == None:
                        self.return_error()

                    user, user_permissions = await CLASS_NAME_KEYDao().get_user_by_id(
                        CLASS_NAME_KEYModel(id=id_user)
                    )

            if user != None:
                if await self._check_permissions(
                    user.id_role, user_permissions, id_funtionality, scope, content
                ):
                    return funtionality, id_login, user

                self.return_not_authorization()

        elif is_auth_needed == self.NOT_AUTH_NEEDED:
            return funtionality, id_login, user

        self.return_not_autenticated()

    # Verifica si un token es autentinco y esta activo. Devuelve id_user
    async def _validate_token(self, token, request):
        try:
            if token:
                token_data = jwt.decode(
                    token, key=self.SECRET_KEY, algorithms=[self.ALGORITHM]
                )

                if (
                    self.JTI in token_data
                    and self.EXP in token_data
                    and self.IAT in token_data
                ):
                    exp = token_data.get(self.EXP)
                    iat = token_data.get(self.IAT)
                    jti = token_data.get(self.JTI)

                    now = datetime.utcnow().timestamp()

                    if exp > now:
                        token_data = Cache.get_token_data(jti)
                        if token_data and len(token_data) == 5:
                            id_user = token_data[0]
                            id_login = token_data[1]
                            id_conn = token_data[2]
                            session_time = token_data[3]
                            scope = token_data[4]

                            if id_user is not None and session_time > now:
                                if Conn.check_request_conn(request, id_conn):
                                    token_data = self._format_cache_token_data(
                                        id_user,
                                        id_login,
                                        id_conn,
                                        self._new_session_time(),
                                        scope,
                                    )
                                    Cache.update_token_data(jti, token_data)
                                    return id_login, id_user, scope
                                else:
                                    # Suplantacion de token o cambio en la ip o la conn expiro de la cache
                                    # Auditar CAMBIO en la IP

                                    # Comprobar si el usuario ha tenido algun login exitoso con la nueva IP, en caso negativo notificar

                                    new_id_conn = await Conn.audit(request)
                                    new_id_login = await Login.new_conn(
                                        request, id_login, new_id_conn
                                    )
                                    token_data = self._format_cache_token_data(
                                        id_user,
                                        new_id_login,
                                        new_id_conn,
                                        self._new_session_time(),
                                        scope,
                                    )
                                    Cache.update_token_data(jti, token_data)

                                    return new_id_login, id_user, scope

                                    # Notificar comportamiento sospechoso
                            else:
                                self.return_session_expired()
                    else:
                        self.return_expired_token()
            else:
                self.return_not_autenticated()

        except JWTError as e:
            print("ERROR: Authorization -> validateToken: JWTError: " + str(e))

        return None, None, None

    # Verifica si un token es valido o no
    def is_valid_token(self, token) -> int:
        try:
            if token:
                token_data = jwt.decode(
                    token, key=self.SECRET_KEY, algorithms=[self.ALGORITHM]
                )

                if (
                    self.JTI in token_data
                    and self.EXP in token_data
                    and self.IAT in token_data
                ):
                    exp = token_data.get(self.EXP)
                    iat = token_data.get(self.IAT)
                    jti = token_data.get(self.JTI)

                    now = datetime.utcnow().timestamp()

                    if exp > now:
                        token_data = Cache.get_token_data(jti)
                        if token_data and len(token_data) == 5:
                            id_user = token_data[0]
                            session_time = token_data[3]

                            if id_user is not None and session_time > now:
                                return True

        except JWTError as e:
            print("ERROR: Authorization -> is_valid_token: JWTError: " + str(e))
            return False

        return None

    # Verifica si un usuario tiene permisos para acceder a un recurso
    async def _check_permissions(
        self, id_role, user_permissions, id_funtionality, user_scope, content
    ):
        try:
            auth_funct = self._check_funtionality(
                id_role, id_funtionality, user_permissions
            )

            role_scope = Cache.get_role_scope(id_role)
            scope = Js.merge_json(role_scope, user_scope)

            auth_scope = self._check_scope(content, scope)

            return True if auth_funct and auth_scope else False

        except Exception as e:
            print("ERROR: Authorization -> check_permissions: " + str(e))

        return False

    # Comprueba todas las key de content, de manera recursiva y si existe
    # alguna key que esta en scope (requiera privilegios) comprueba si tiene alcance para ese recurso

    """
       Para futuro: crear una blacklist y whitelist por cada alcance 
       Ahora mismo es una whitelist: que si el valor no esta en role_scope o user_scope no autoriza
       A futuro: Crear un nuevo atributo en la tabla role_scope y user_scope de la BBDD que determine
                 si ese valor es de blacklist o de whitelist (1 o 0) por ejemplo.
                 
                 Una vez que los valores de estas tablas estan declarados como de whitelist o de blacklist 
                 
                 Configurar el formato de la respuesta a la consulta de scope en los DAO con el nuevo parametro [white_list | black_list]
                 
                 Añadir la comparacion de la blacklist en:
                 
                 
                 
                 if (item not in user_scope[key][white_list] and item not in role_scope[key][white_list]) or 
                    (item in user_scope[key][black_list] or item in role_scope[key][black_list])
                 
                 if (value not in user_scope[key][white_list] and value not in role_scope[key][white_list]) or
                    (value in user_scope[key][black_list] or value in role_scope[key][black_list])
                 
                 Si no hay nada en white_list o black_list NO autoriza
                 Si hay en white_list y black_list, predomina black_list, NO autoriza
                 
                 Solo autoriza si esta unicamente en white_list
                 
    """

    def _check_scope(self, content, scope):
        if content:
            for key, value in content.items():
                if isinstance(value, dict):
                    # Si el valor es un diccionario, realizar una llamada recursiva
                    if not self._check_scope(value, scope):
                        return False

                elif isinstance(value, list):
                    if key in scope:  # Si la key de la lista esta en scope
                        # Comprobar todos los elementos de la lista
                        for item in value:
                            if item not in scope[key]:
                                return False

                else:
                    if key in scope:
                        # Si el valor es un valor único, comprobar si está en el alcance correspondiente
                        if value not in scope[key]:
                            return False

        # Si ninguna clave coincide o no hay contenido, devolver True
        return True

    # Verifica si un usuario tiene permisos para acceder a un recurso
    def _check_funtionality(self, id_role, id_funtionality, user_permissions):
        try:
            # Permisos otorgados por el rol
            role_permissions = Cache.get_role_permissions(id_role)

            # Permisos posibles para acceder a la funcionalidad
            funtionality_permissions = Cache.get_funtionality_permissions(
                id_funtionality
            )

            # print("user_permissions" + str(user_permissions))
            # print("role_permissions" + str(role_permissions))
            # print("funtionality_permissions" + str(funtionality_permissions))

            if role_permissions and funtionality_permissions:
                rol_funcionality = set(role_permissions) & set(funtionality_permissions)
                if rol_funcionality:
                    return True

            if user_permissions and funtionality_permissions:
                user_funcionality = set(user_permissions) & set(
                    funtionality_permissions
                )
                if user_funcionality:
                    return True

        except Exception as e:
            print("ERROR: Authorization -> check_funtionality: " + str(e))

        return False

    # Crea un nuevo token
    def _create_token(self, jti):
        try:
            exp = datetime.utcnow() + timedelta(seconds=Cache.TIME_TOKEN_EXPIRES)
            iat = datetime.utcnow()

            data = {self.JTI: str(jti), self.IAT: iat, self.EXP: exp}
            return jwt.encode(data, key=self.SECRET_KEY, algorithm=self.ALGORITHM)

        except Exception as e:
            print("ERROR: Authorization -> createToken: " + str(e))

        return None

    def _check_jti_cache(self, jti):
        return True if jti and not Cache.get_token_data(jti) else False

    def _update_token_data(self, jti, token_data):
        return True if Cache.update_token_data(jti, token_data) else False

    # Actualiza el tiempo de sesion de un token, ademas de la informacion del usuario
    def _new_session_time(self):
        try:
            date = datetime.utcnow() + timedelta(minutes=self.TIME_SESSION_EXPIRES)
            timestamp = date.timestamp()
            return timestamp
        except Exception as e:
            print("ERROR: Authorization -> new_session_time: " + str(e))

        return None

    def _format_cache_token_data(self, id_user, id_login, id_conn, session_time, scope):
        return [id_user, id_login, id_conn, session_time, scope]
