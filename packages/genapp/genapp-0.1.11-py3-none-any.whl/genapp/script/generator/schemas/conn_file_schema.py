import asyncio
from datetime import datetime, timedelta

from app.CRUD_KEY.DATABASE_NAME_KEY.API_AUDIT_REQUEST_NOT_LOGGED_KEY_dao import (
    API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEYDao,
)
from app.CRUD_KEY.DATABASE_NAME_KEY.API_CONNECTION_KEY_dao import (
    API_CONNECTION_CLASS_KEYDao,
)
from app.CRUD_KEY.DATABASE_NAME_KEY.API_FUNTIONALITY_KEY_dao import (
    API_FUNTIONALITY_CLASS_KEYDao,
)
from app.CRUD_KEY.DATABASE_NAME_KEY.API_LOGIN_KEY_dao import API_LOGIN_CLASS_KEYDao
from app.external_api.ip_geo import IpGeo, IpGeoKeys
from app.MODEL_KEY.DATABASE_NAME_KEY.API_AUDIT_REQUEST_NOT_LOGGED_KEY import (
    API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEYModel,
)
from app.MODEL_KEY.DATABASE_NAME_KEY.API_CONNECTION_KEY import (
    API_CONNECTION_CLASS_KEYModel,
)
from app.MODEL_KEY.DATABASE_NAME_KEY.API_LOGIN_KEY import API_LOGIN_CLASS_KEYModel
from app.util import date as Dt
from app.util import request as Rq
from app.service import cache as Cache

from urllib.parse import urlparse


class ConnKeys:
    IS_BOT_KEY = "is_bot"
    IS_BOT = 1
    TIMESTAMP = "timestamp"
    KEY = "key"
    URL = "url"
    BLOCKED = 1
    ALLOW = 0

    BOT = "BT"
    SEQUENTIAL = "SE"
    FAST = "FA"
    BAD_METHOD = "BM"
    HACKER = "HK"
    ALTER_TOKEN = "AT"
    ENUMERATING = "EN"


class Conn:
    # Segundos para coger los intentos entre el intervalo (hace 300s - ahora)
    ANALYZE_LOGIN_TIME = 300
    ANALYZE_REQUEST_NOT_LOGGED_TIME = 10

    # Segundos, Si en dos segundos hay mas de 4 request a endpoints distintos..
    ANALYZE_IS_ENUMERATING_TIME = 1
    # Intentos maximos para considerar enumeracion
    ANALYZE_IS_ENUMERATING_ATTEMPS = 3

    ANALYZE_SECUENCIAL_ERROR = 0.3  # Segundos
    ANALYZE_SECUENCIAL_ATTEMPS = 3  # Muestreo de intentos minimos
    ANALYZE_SECUENCIAL_MAX_FRECUENCY = 4  # Intentos Secuenciales

    ANALYZE_IS_FAST_ATTEMPS = 4  # Intentos
    ANALYZE_IS_FAST_TIME = 3  # Segundos

    def check_request_conn(request, id_conn) -> bool:
        try:
            ip = Rq.get_ip(request)
            conn = Cache.get_connection_data(ip)

            # Se ha cambiado la IP puesto que la conexion no esta registrada
            if not conn:
                return False

            # Si la Conexion (IP) de la solitud coincide con el id_conn del asociado al token
            return conn[1] == id_conn

        except Exception as e:
            print("ERROR: Auth Conn -> check_request_conn: " + str(e))

    async def get_connection(request) -> int:
        try:
            # await asyncio.sleep(0.5)
            ip = Rq.get_ip(request)
            conn = Cache.get_connection_data(ip)

            if not conn:
                return await Conn.audit(request)

            status = conn[0]
            id_conn = conn[1]
            country_code = conn[2]

            if status == ConnKeys.ALLOW:
                return id_conn

            elif status == ConnKeys.BLOCKED:
                return None

        except Exception as e:
            print("ERROR: Auth Conn -> get_connection: " + str(e))

    #####################################################
    #                  Auditar Conexion                 #
    #####################################################
    async def audit(request) -> int:
        try:
            ip = Rq.get_ip(request)
            id_conn = await Conn._new_conn_id(ip)

            asyncio.create_task(
                Conn._update_conn(ip, id_conn)
            )  # No es necesario esperar a que guarde la conexion si no existe
            return id_conn

        except Exception as e:
            print("ERROR: Auth Conn -> audit " + str(e))

    async def _update_conn(ip, id_conn) -> None:
        try:
            ip_geo = await IpGeo().get_data(ip)
            country_code = None
            zip_code = None
            if ip_geo:
                country_code = ip_geo.get(IpGeoKeys.COUNTRY_CODE2, None)
                zip_code = ip_geo.get(IpGeoKeys.ZIPCODE, None)

            cache_data = Cache.get_connection_data(ip)

            conn_data = Conn.format_cache_conn_data(
                cache_data[0], id_conn, country_code
            )
            Cache.update_connection_data(ip, conn_data)

            dto = API_CONNECTION_CLASS_KEYModel(
                id=id_conn,
                country_code=country_code,
                zip_code=zip_code,
            )

            await API_CONNECTION_CLASS_KEYDao().update(dto)

        except Exception as e:
            print("ERROR: Auth Conn -> update_connection: " + str(e))

    async def _new_conn_id(ip) -> int:
        try:
            dto = API_CONNECTION_CLASS_KEYModel(
                ip=ip,
                timestamp=Dt.get_str_timestamp(),
                block=ConnKeys.ALLOW,
            )
            conn = await API_CONNECTION_CLASS_KEYDao().insert(dto)

            if conn:
                # Si se añade la un nueva conexion a BBDD inmediatamente se introduce en cache
                cache_data = Conn.format_cache_conn_data(ConnKeys.ALLOW, conn.id, None)
                Cache.update_connection_data(ip, cache_data)

                return conn.id

        except Exception as e:
            print("ERROR: Auth Conn -> new_connection_id: " + str(e))

    #####################################################
    #                Analisis de Conexion               #
    #####################################################
    async def analyze_request_not_logged(request, id_conn) -> None:
        try:
            dto = API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEYModel(id_conn=id_conn)
            firts_attemp = datetime.utcnow() - timedelta(
                seconds=Conn.ANALYZE_REQUEST_NOT_LOGGED_TIME
            )

            attempts = await API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEYDao().last_requests_not_logged(
                dto, firts_attemp
            )

            attempts = Conn._filter_distinct_attemps(attempts, ConnKeys.URL)

            funtionalities = (
                await API_FUNTIONALITY_CLASS_KEYDao().get_no_auth_funtionalities()
            )
            urls_allow = Conn._get_urls_allow(funtionalities)
            attempts = Conn._filter_allow_urls(attempts, urls_allow)

            if Conn._is_enumerating(attempts):
                await Conn.block_conn(request, id_conn, ConnKeys.ENUMERATING)

        except Exception as e:
            print("ERROR: Auth Conn -> analyze_request_not_logged: " + str(e))

    async def analyze_login(request, id_conn) -> None:
        try:
            dto = API_LOGIN_CLASS_KEYModel(id_conn=id_conn)
            firts_attemp = datetime.utcnow() - timedelta(
                seconds=Conn.ANALYZE_LOGIN_TIME
            )

            attempts, _ = await API_LOGIN_CLASS_KEYDao().last_logins(dto, firts_attemp)
            attempts = Conn._filter_distinct_attemps(attempts, ConnKeys.KEY)

            if Conn._is_fast(attempts):
                await Conn.block_conn(request, id_conn, ConnKeys.FAST)

            elif Conn._is_sequential(attempts):
                await Conn.block_conn(request, id_conn, ConnKeys.SEQUENTIAL)

            elif Conn._is_bot(attempts):
                await Conn.block_conn(request, id_conn, ConnKeys.BOT)

        except Exception as e:
            print("ERROR: Auth Conn -> analyze_login: " + str(e))

    def _filter_distinct_attemps(attempts, key_filter):
        try:
            distinct_attemps = []
            keys = []

            for attempt in attempts:
                key = attempt[key_filter]
                # Verificar si la clave ya ha sido encontrada
                if key not in keys:
                    # Si la clave es nueva, agregar el JSON a la lista filtrada y añadir la clave al conjunto
                    distinct_attemps.append(attempt)
                    keys.append(key)

            return distinct_attemps

        except Exception as e:
            print("ERROR: Auth Conn -> filter_distinct_attempps: " + str(e))

    def _filter_allow_urls(attempts, urls_allow):
        try:
            # Lista para almacenar las URLs no permitidas
            not_allowed_attempts = []

            for attempt in attempts:
                url_path = urlparse(attempt["url"]).path.strip("/")

                # Si la ruta empieza por public se omite
                if url_path.startswith("public"):
                    continue

                # Si necesita autorizacion o no existe
                if not url_path in urls_allow:
                    not_allowed_attempts.append(attempt)
            return not_allowed_attempts

        except Exception as e:
            print("ERROR: Auth Conn -> _filter_allow_urls: " + str(e))
            return []

    def _get_urls_allow(functionalities):
        try:
            urls = []
            for functionality in functionalities:
                segments = []

                if functionality.segment_1 is not None:
                    segments.append(str(functionality.segment_1))

                if functionality.segment_2 is not None:
                    segments.append(str(functionality.segment_2))

                if functionality.segment_3 is not None:
                    segments.append(str(functionality.segment_3))

                if functionality.segment_4 is not None:
                    segments.append(str(functionality.segment_4))

                url = "/".join(segments)
                urls.append(url)

            return urls

        except Exception as e:
            print("ERROR: Auth Conn -> get_urls_allow: " + str(e))

    # Comprueba si existe un patron de tiempo entre los intentos
    def _is_enumerating(attempts):
        try:
            if len(attempts) < Conn.ANALYZE_IS_ENUMERATING_ATTEMPS:
                return False
            attempts.sort(key=lambda x: x[ConnKeys.TIMESTAMP])

            start_time = attempts[0][ConnKeys.TIMESTAMP]
            end_time = attempts[-1][ConnKeys.TIMESTAMP]
            timeframe = (end_time - start_time).total_seconds()

            if timeframe <= Conn.ANALYZE_IS_ENUMERATING_TIME:
                return True

        except Exception as e:
            print("ERROR: Auth Conn -> is_enumerating: " + str(e))

    def _is_sequential(attempts) -> bool:
        try:
            timestamps = [entry[ConnKeys.TIMESTAMP] for entry in attempts]
            if len(timestamps) < Conn.ANALYZE_SECUENCIAL_ATTEMPS:
                return False

            # Calcular diferencias de tiempo entre cada par de timestamps
            diff_list = [
                (timestamps[i] - timestamps[i + 1]).total_seconds()
                for i in range(len(timestamps) - 1)
            ]
            list_copy = diff_list.copy()

            frecuency = 0

            for diff_x in diff_list:
                list_copy.pop(0)
                for diff_y in list_copy:
                    diff = abs(abs(diff_x) - abs(diff_y))
                    if diff <= Conn.ANALYZE_SECUENCIAL_ERROR:
                        frecuency += 1
                        break

            return True if frecuency >= Conn.ANALYZE_SECUENCIAL_MAX_FRECUENCY else False

        except Exception as e:
            print("ERROR: Auth Conn -> is_secuencial: " + str(e))

        return False

    # Comprueba si los intentos se han realizado muy rapido
    def _is_fast(attempts) -> bool:
        try:
            if len(attempts) < Conn.ANALYZE_IS_FAST_ATTEMPS:
                return False

            # attempts.sort(key=lambda x: x[ConnKeys.TIMESTAMP])

            # for i in range(len(attempts) - Conn.ANALYZE_IS_FAST_ATTEMPS + 1):
            #     start_time = attempts[i][ConnKeys.TIMESTAMP]
            #     end_time = attempts[i + Conn.ANALYZE_IS_FAST_ATTEMPS - 1][
            #         ConnKeys.TIMESTAMP
            #     ]
            #     timeframe = (end_time - start_time).total_seconds()

            #     if timeframe <= Conn.ANALYZE_IS_FAST_TIME:
            #         return True

            attempts.sort(key=lambda x: x[ConnKeys.TIMESTAMP])

            start_time = attempts[0][ConnKeys.TIMESTAMP]
            end_time = attempts[-1][ConnKeys.TIMESTAMP]
            timeframe = (end_time - start_time).total_seconds()

            if timeframe <= Conn.ANALYZE_IS_FAST_TIME:
                return True

        except Exception as e:
            print("ERROR: Auth Conn -> is_fast: " + str(e))

        return False

    # Comprueba si los intentos los ha realizado un bot
    def _is_bot(attempts) -> bool:
        try:
            is_bot_attemps = [entry[ConnKeys.IS_BOT_KEY] for entry in attempts]

            return ConnKeys.IS_BOT in is_bot_attemps

        except Exception as e:
            print("ERROR: Auth Conn -> _is_bot: " + str(e))

        return False

    async def block_conn(request, id_conn, reason=None) -> None:
        """
        Bloquea una IP en BBDD y Cache

        Args:
            request (Request): request par obtener la IP a bloquear (Para bloquear en cache)
            id_conn (int): id de conn en BBDD (Para bloquear en BBDD)
        """
        try:
            ip = Rq.get_ip(request)
            # Se comprueba primero si esta permitida en cache por si hay varias intentos simultaneos
            conn = Cache.get_connection_data(ip)
            if conn[0] == ConnKeys.ALLOW:
                print("IP: ", ip, "  Blocked")
                cache_data = Conn.format_cache_conn_data(
                    ConnKeys.BLOCKED, id_conn, None
                )
                Cache.update_connection_data(ip, cache_data)

                dto = API_CONNECTION_CLASS_KEYModel(
                    id=id_conn, block=ConnKeys.BLOCKED, reason=reason
                )
                await API_CONNECTION_CLASS_KEYDao().update(dto)

        except Exception as e:
            print("ERROR: Auth Conn -> block_conn: " + str(e))

    def format_cache_conn_data(status, id_conn=None, country_code=None) -> list:
        return [status, id_conn, country_code]
