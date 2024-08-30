import asyncio
from threading import Lock

from cachetools import TTLCache
from app.crud.genericapp.connection_dao import (
    ConnectionDao,
)
from app.crud.genericapp.funtionality_dao import (
    FuntionalityDao,
)
from app.crud.genericapp.role_dao import RoleDao

from app.crud.schema.schema_genericapp import Funtionality

from app.util import date as Dt

TIME_FUNTIONALITY_PERMISSIONS = 60
TIME_FUNTIONALITY = 51
TIME_ROLE_PERMISSIONS = 45
TIME_ROLE_SCOPE = 55

# Tiempo que se tarda en desbloquear una conexion en cache
# Tiempo que se tarda en caducar una conexion y se renueva
TIME_CONNECTION_EXPIRES = 121600

# Tiempo desde el que cargara conexiones desde la BBDD
TIME_LOAD_CONNECTION = 21600

# Tiempo en segundos para la expiracion del token
TIME_TOKEN_EXPIRES = 86400

TIME_EXTERNAL_API_TOKEN_EXPIRE = 86400

extenal_api_token_cache = TTLCache(maxsize=1000, ttl=TIME_EXTERNAL_API_TOKEN_EXPIRE)
extenal_api_token_cache_lock = Lock()
"""
{
    identificador de api (Nombre del fichero de conexión) : "token.jwt.api"
}
"""


# Cache de los token activos del sistema
token_data_cache = TTLCache(maxsize=1000, ttl=TIME_TOKEN_EXPIRES)
token_data_cache_lock = Lock()

"""
{
    identificador de token (jti) : {
        id_user : identificador de usuario,
        session_time : timestamp final,
        scope : ['ATALAYA', ...]
    }
}
"""

# Cache para los permisos que hacen falta para acceder a una funcionalidad
funtionality_permissions_cache = TTLCache(maxsize=5000, ttl=86400)
funtionality_permissions_cache_lock = Lock()


# Cache para las conexiones que estan bloqueadas o no
connection_cache = TTLCache(maxsize=5000, ttl=TIME_CONNECTION_EXPIRES)
connection_cache_lock = Lock()
"""
{
    ip : [id_conn, country_code, ALLOW | BLOCKED],
    ...
}
"""

# Cache para los permisos que tiene cada rol
role_permissions_cache = TTLCache(maxsize=1000, ttl=86400)
role_permissions_cache_lock = Lock()

# Cache para los scope que tiene cada rol
role_scope_cache = TTLCache(maxsize=1000, ttl=86400)
role_scope_cache_lock = Lock()
"""
{
    0 : {
        "cod_uf" : [],
        "att" : [], ... 
    },
    
    1 : {
        "cod_uf" : [],
        "att" : [], ... 
    },
    
}
"""

# Cache para las funcionalidades dadas de alta en el sistema
funtionalities_cache = TTLCache(maxsize=1000, ttl=86400)
funtionalities_cache_lock = Lock()


############################################################
################# CACHE EXTERNAL API TOKEN #################
############################################################
def update_extenal_api_token(aid: str, token):
    try:
        with extenal_api_token_cache_lock:
            if token:
                extenal_api_token_cache[aid] = token
            else:
                extenal_api_token_cache.pop(aid)
            return True
    except Exception as e:
        print("ERROR: Cache -> update_extenal_api_token: " + str(e))

    return False


def get_extenal_api_token(aid: str) -> dict:
    try:
        with extenal_api_token_cache_lock:
            if aid in extenal_api_token_cache:
                return extenal_api_token_cache.get(aid, None)

    except Exception as e:
        print("ERROR: Cache -> get_extenal_api_token: " + str(e))

    return None


############################################################
##################### CACHE TOKEN DATA #####################
############################################################
def update_token_data(jti: str, token_data):
    try:
        with token_data_cache_lock:
            token_data_cache[jti] = token_data
            return True
    except Exception as e:
        print("ERROR: Cache -> update_token_data: " + str(e))

    return False


def get_token_data(jti: str) -> dict:
    try:
        with token_data_cache_lock:
            if jti in token_data_cache:
                return token_data_cache.get(jti, [])

    except Exception as e:
        print("ERROR: Cache -> get_token_data: " + str(e))

    return None


############################################################
###################### CACHE CONNECTION ####################
############################################################
def update_connection_data(ip: str, connection_data):
    try:
        with connection_cache_lock:
            connection_cache[ip] = connection_data
            return True
    except Exception as e:
        print("ERROR: Cache -> update_connection_data: " + str(e))

    return False


def get_connection_data(ip: str) -> dict:
    try:
        with connection_cache_lock:
            if ip in connection_cache:
                return connection_cache.get(ip, [])

    except Exception as e:
        print("ERROR: Cache -> get_connection_data: " + str(e))

    return None


# Carga las ultimas conexiones desde hace TIME_CONNECTION_EXPIRES segundos
async def load_connection_data():
    try:
        _, timestamp_delta = Dt.get_timestamps_now_delta(-1 * TIME_LOAD_CONNECTION)
        result = await ConnectionDao().get_last_connections(
            timestamp_delta
        )

        if result:
            with connection_cache_lock:
                for key, value in result.items():
                    connection_cache[key] = value
                return True

    except Exception as e:
        print("ERROR: Cache -> load_connection_data: " + str(e))

    return False


############################################################
################### CACHE ROLE PERMISSIONS #################
############################################################
def get_role_permissions(id_role) -> list:
    try:
        with role_permissions_cache_lock:
            return role_permissions_cache.get(id_role, [])
    except Exception as e:
        print("ERROR: Cache -> get_role_permissions: " + str(e))

    return None


async def update_role_permissions() -> bool:
    try:
        result = await RoleDao().get_all_permissions()

        with role_permissions_cache_lock:
            for key, value in result.items():
                role_permissions_cache[key] = value
            return True

    except Exception as e:
        print("ERROR: Cache -> update_role_permissions: " + str(e))

    return False


############################################################
###################### CACHE ROLE SCOPE ####################
############################################################
def get_role_scope(id_role) -> list:
    try:
        with role_scope_cache_lock:
            return role_scope_cache.get(id_role, [])
    except Exception as e:
        print("ERROR: Cache -> get_role_scope: " + str(e))

    return None


async def update_role_scope() -> bool:
    try:
        result = await RoleDao().get_all_scopes()

        with role_scope_cache_lock:
            for key, value in result.items():
                role_scope_cache[key] = value
            return True

    except Exception as e:
        print("ERROR: Cache -> update_role_scope: " + str(e))

    return False


############################################################
############## CACHE FUNTIONALITY PERMISSIONS ##############
############################################################
def get_funtionality_permissions(id_funtionality) -> list:
    try:
        with funtionality_permissions_cache_lock:
            return funtionality_permissions_cache.get(id_funtionality, [])
    except Exception as e:
        print("ERROR: Cache -> get_funtionality_permissions: " + str(e))

    return None


async def update_funtionality_permissions() -> bool:
    try:
        result = await FuntionalityDao().get_all_permissions()

        with funtionality_permissions_cache_lock:
            for key, value in result.items():
                funtionality_permissions_cache[key] = value
            return True

    except Exception as e:
        print("ERROR: Cache -> update_funtionality_permissions: " + str(e))

    return False


############################################################
##################### CACHE FUNTIONALITY ###################
############################################################
def get_id_funtionality(
    segment_1, segment_2=None, segment_3=None, segment_4=None
) -> int:
    try:
        keys = [segment_1, segment_2, segment_3, segment_4]

        with funtionalities_cache_lock:
            data = funtionalities_cache

            for i, key in enumerate(keys):
                if key in data:
                    data = data.get(key)
                    if isinstance(data, Funtionality):
                        if i + 1 < len(
                            keys
                        ):  # Para funcionalidades que NO tienen las 4 keys
                            if keys[i + 1] is None:
                                return data
                            else:
                                return None
                        else:  # Para las funcionalidades que SI tienen las 4 keys
                            return data
                else:
                    return None
            return None

    except Exception as e:
        print(f"ERROR: Cache -> get_funtionality: {e}")

    return None


async def update_funtionalities() -> bool:
    try:
        result = await FuntionalityDao().get_all_funtionalities()

        with funtionalities_cache_lock:
            for key, value in result.items():
                funtionalities_cache[key] = value
            return True

    except Exception as e:
        print("ERROR: Cache -> update_funtionality: " + str(e))

    return False


###################################################
#  Ejecuccion de funciones ciclicas  asincronas  ##
###################################################
async def async_update_funtionality_permissions():
    try:
        while True:
            await update_funtionality_permissions()
            await asyncio.sleep(TIME_FUNTIONALITY_PERMISSIONS)

    except Exception as e:
        print("ERROR: Cache -> async_update_funtionality_permissions: " + str(e))


async def async_update_role_permissions():
    try:
        while True:
            await update_role_permissions()
            await asyncio.sleep(TIME_ROLE_PERMISSIONS)

    except Exception as e:
        print("ERROR: Cache -> async_update_role_permissions: " + str(e))


async def async_update_role_scope():
    try:
        while True:
            await update_role_scope()
            await asyncio.sleep(TIME_ROLE_SCOPE)

    except Exception as e:
        print("ERROR: Cache -> async_update_role_scope: " + str(e))


async def async_update_funtionalities():
    try:
        while True:
            await update_funtionalities()
            await asyncio.sleep(TIME_FUNTIONALITY)

    except Exception as e:
        print("ERROR: Cache -> async_update_funtionalities: " + str(e))
