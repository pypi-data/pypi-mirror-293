import inspect
from threading import Lock

from cachetools import TTLCache
from CRUD_KEY.DATABASE_NAME_KEY import (API_FUNTIONALITY_KEY_dao,
                                        API_ROLE_KEY_dao, API_USER_KEY_dao)
from DATABASE_KEY.listener import funtionality as FntListener
from DATABASE_KEY.listener import \
    funtionality_permission as FntPermissionListener
from DATABASE_KEY.listener import role_permission as RolePermissionListener
from MODEL_KEY.DATABASE_NAME_KEY import API_FUNTIONALITY_KEY, API_USER_KEY

FuntionalityDao = None
UserDao = None
RoleDao = None

UserModel = None
FuntionalityModel = None

TIME_FUNTIONALITY_PERMISSIONS = 60

TIME_FUNTIONALITY = 51
TIME_ROLE_PERMISSIONS = 45

# Cache de los usuarios que se han loggeado con exito
users_logged_cache = TTLCache(maxsize=1000, ttl=300)
users_cache_lock = Lock()

# Cache para los permisos que hacen falta para acceder a una funcionalidad
funtionality_permissions_cache = TTLCache(maxsize=1000, ttl=86400)
funtionality_permissions_cache_lock = Lock()

# Cache para los permisos que tiene cada rol
role_permissions_cache = TTLCache(maxsize=1000, ttl=86400)
role_permissions_cache_lock = Lock()

# Cache para las funcionalidades dadas de alta en el sistema
funtionalities_cache = TTLCache(maxsize=1000, ttl=86400)
funtionalities_cache_lock = Lock()


def check_user(id_user):
    try:
        return True if id_user in users_logged_cache else False

    except Exception as e:
        print("ERROR: Cache -> check_user_cache: " + str(e))

    return False


def update_user(id_user, data=None):
    try:
        if not data:
            user = UserModel(id=id_user)
            result = UserDao().getUserById(user)
        else:
            result = data

        if result:
            with users_cache_lock:
                users_logged_cache[id_user] = result

        return True if result else False

    except Exception as e:
        print("ERROR: Cache -> update_user: " + str(e))

    return False


def get_user(id_user) -> dict:
    try:
        with users_cache_lock:
            return users_logged_cache.get(id_user, {})
    except Exception as e:
        print("ERROR: Cache -> get_user: " + str(e))

    return None


def get_role_permissions(id_role) -> list:
    try:
        with role_permissions_cache_lock:
            return role_permissions_cache.get(id_role, [])
    except Exception as e:
        print("ERROR: Cache -> get_role_permissions: " + str(e))

    return None


def get_funtionality_permissions(id_funtionality) -> list:
    try:
        with funtionality_permissions_cache_lock:
            return funtionality_permissions_cache.get(id_funtionality, [])
    except Exception as e:
        print("ERROR: Cache -> get_funtionality_permissions: " + str(e))

    return None


def get_id_funtionality(object) -> int:
    try:
        keys = [object.name, object.database, object.crud_type, object.table]

        with funtionalities_cache_lock:
            data = funtionalities_cache

            for i, key in enumerate(keys):
                if key in data:
                    data = data.get(key)
                    if isinstance(data, int):
                        if i + 1 < len(keys):  # Para funcionalidades que NO tienen las 4 keys
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


def update_role_permissions():
    try:
        result = RoleDao().getAllPermissions()

        with role_permissions_cache_lock:
            for key, value in result.items():
                role_permissions_cache[key] = value

    except Exception as e:
        print("ERROR: Cache -> update_role_permissions: " + str(e))


def update_funtionality_permissions():
    try:
        result = FuntionalityDao().getAllPermissions()

        with funtionality_permissions_cache_lock:
            for key, value in result.items():
                funtionality_permissions_cache[key] = value

    except Exception as e:
        print("ERROR: Cache -> update_funtionality_permissions: " + str(e))


def update_funtionalities():
    try:
        result = FuntionalityDao().getAllFuntionalities()

        with funtionalities_cache_lock:
            for key, value in result.items():
                funtionalities_cache[key] = value

    except Exception as e:
        print("ERROR: Cache -> update_funtionality_permissions: " + str(e))


def init():
    global FuntionalityDao, UserDao, RoleDao, UserModel, FuntionalityModel
    try:
        # Dao class imports
        classes_funtionality_dao = inspect.getmembers(
            API_FUNTIONALITY_KEY_dao, inspect.isclass)
        f_dao = [cls for cls in classes_funtionality_dao if cls[1].__module__ ==
                 API_FUNTIONALITY_KEY_dao.__name__]
        if f_dao:
            _, FuntionalityDao = f_dao[0]

        classes_user_dao = inspect.getmembers(
            API_USER_KEY_dao, inspect.isclass)
        u_dao = [cls for cls in classes_user_dao if cls[1].__module__ ==
                 API_USER_KEY_dao.__name__]
        if u_dao:
            _, UserDao = u_dao[0]

        classes_role_dao = inspect.getmembers(
            API_ROLE_KEY_dao, inspect.isclass)
        r_dao = [cls for cls in classes_role_dao if cls[1].__module__ ==
                 API_ROLE_KEY_dao.__name__]
        if r_dao:
            _, RoleDao = r_dao[0]

        # Model class imports
        classes_funtionality_model = inspect.getmembers(
            API_FUNTIONALITY_KEY, inspect.isclass)
        f_model = [cls for cls in classes_funtionality_model if cls[1].__module__ ==
                   API_FUNTIONALITY_KEY.__name__]
        if f_model:
            _, FuntionalityModel = f_model[0]

        classes_user_model = inspect.getmembers(API_USER_KEY, inspect.isclass)
        u_model = [
            cls for cls in classes_user_model if cls[1].__module__ == API_USER_KEY.__name__]
        if u_model:
            _, UserModel = u_model[0]

        update_funtionalities()
        FntListener.init(callback=update_funtionalities)

        update_funtionality_permissions()
        FntPermissionListener.init(callback=update_funtionality_permissions)

        update_role_permissions()
        RolePermissionListener.init(callback=update_role_permissions)

        print("Cache initialized successfully")

    except Exception as e:
        print("ERROR: Cache -> init: " + str(e))
    # Configura y inicia el programador de tareas APScheduler
