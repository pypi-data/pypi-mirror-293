from cachetools import TTLCache
from threading import Lock


TIME_RECOVERY_PASSWD_CODE_EXPIRE = 90

recovery_passwd_code_cache = TTLCache(
    maxsize=5000, ttl=TIME_RECOVERY_PASSWD_CODE_EXPIRE
)
recovery_passwd_code_cache_lock = Lock()
"""
{
    email : code
}
"""


TIME_RECOVERY_PASSWD_TOKEN_EXPIRE = 21600

recovery_passwd_token_cache = TTLCache(
    maxsize=5000, ttl=TIME_RECOVERY_PASSWD_TOKEN_EXPIRE
)
recovery_passwd_token_cache_lock = Lock()
"""
{
    email : token
}
"""

TIME_CONFIRM_ACCOUNT_EXPIRE = 21600

confirm_account_cache = TTLCache(maxsize=5000, ttl=TIME_CONFIRM_ACCOUNT_EXPIRE)
confirm_account_cache_lock = Lock()
"""
{
    email : code
}
"""


############################################################
################ CACHE RECOVERY PASSWD CODE ################
############################################################
def update_confirm_account_code(email: str, code: str):
    try:
        with confirm_account_cache_lock:
            if email:
                confirm_account_cache[email] = code

                return True
    except Exception as e:
        print("ERROR: Cache Bis -> update_confirm_account_code: " + str(e))

    return False


def get_confirm_account_code(email: str) -> str:
    try:
        with confirm_account_cache_lock:
            if email in confirm_account_cache:
                return confirm_account_cache.get(email, None)

    except Exception as e:
        print("ERROR: Cache Bis -> get_confirm_account_code: " + str(e))

    return None


def pop_confirm_account_code(email: str) -> str:
    try:
        with confirm_account_cache_lock:
            if email in confirm_account_cache:
                confirm_account_cache.pop(email)
                return True

    except Exception as e:
        print("ERROR: Cache Bis -> pop_confirm_account_code: " + str(e))

    return False


############################################################
################ CACHE RECOVERY PASSWD CODE ################
############################################################
def update_recovery_passwd_code(email: str, code: str):
    try:
        with recovery_passwd_code_cache_lock:
            if email:
                recovery_passwd_code_cache[email] = code

                return True
    except Exception as e:
        print("ERROR: Cache Bis -> update_recovery_passwd_code: " + str(e))

    return False


def get_recovery_passwd_code(email: str) -> str:
    try:
        with recovery_passwd_code_cache_lock:
            if email in recovery_passwd_code_cache:
                return recovery_passwd_code_cache.get(email, None)

    except Exception as e:
        print("ERROR: Cache Bis -> get_recovery_passwd_code: " + str(e))

    return None


############################################################
################ CACHE RECOVERY PASSWD TOKEN ###############
############################################################
def update_recovery_passwd_token(email: str, token: str):
    try:
        with recovery_passwd_token_cache_lock:
            if email:
                recovery_passwd_token_cache[email] = token

                return True

    except Exception as e:
        print("ERROR: Cache Bis -> update_recovery_passwd_token: " + str(e))

    return False


def get_recovery_passwd_token(email: str) -> str:
    try:
        with recovery_passwd_token_cache_lock:
            if email in recovery_passwd_token_cache:
                return recovery_passwd_token_cache.get(email, None)

    except Exception as e:
        print("ERROR: Cache Bis -> get_recovery_passwd_token: " + str(e))

    return None
