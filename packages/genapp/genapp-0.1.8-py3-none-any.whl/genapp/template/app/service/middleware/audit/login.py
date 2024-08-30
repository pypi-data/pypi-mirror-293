from app.crud.genericapp.login_dao import LoginDao
from device_detector import DeviceDetector
from fastapi.encoders import jsonable_encoder
from app.model.genericapp.login import LoginModel

from app.util import date as Dt


class LoginStatus:
    OK = 1
    DENY = 0


class Login:

    async def audit(id_conn, status, request, username, passwd, id_user=None):
        try:
            timestamp = Dt.get_str_timestamp()

            is_bot, device_type, device_brand, device_model, os_name, os_version = (
                Login._dump_user_agent(request)
            )

            dto = LoginModel(
                id_user=id_user,
                id_conn=id_conn,
                username=username,
                key=passwd,
                timestamp=timestamp,
                is_bot=is_bot,
                device_type=device_type,
                device_brand=device_brand,
                device_model=device_model,
                os_name=os_name,
                os_version=os_version,
                status=status,
            )

            login = await LoginDao().insert(dto)

            if login:
                return login.id

        except Exception as e:
            print("ERROR: Audit Login -> audit: " + str(e))

    # Audita una nuevo login para una nueva conexion
    async def new_conn(request, id_login, new_id_conn):
        try:
            dto = LoginModel(id=id_login)
            old_login, _ = await LoginDao().query(dto)
            old_login = old_login[0]
            if old_login:
                timestamp = Dt.get_str_timestamp()

                is_bot, device_type, device_brand, device_model, os_name, os_version = (
                    Login._dump_user_agent(request)
                )

                dto = LoginModel(
                    id_user=old_login["id_user"],
                    id_conn=new_id_conn,
                    username=old_login["username"],
                    key=old_login["key"],
                    timestamp=timestamp,
                    is_bot=is_bot,
                    device_type=device_type,
                    device_brand=device_brand,
                    device_model=device_model,
                    os_name=os_name,
                    os_version=os_version,
                    status=LoginStatus.OK,
                )

                login = await LoginDao().insert(dto)

                if login:
                    print(
                        "Audit Login -> new_conn: se cambia la IP notificar comportamiento sospechoso al usuario via email"
                    )
                    return login.id

        except Exception as e:
            print("ERROR: Audit Login -> new_conn: " + str(e))

    def _dump_user_agent(request):
        try:
            user_agent = request.headers.get("User-Agent")
            device_detector = DeviceDetector(user_agent)
            device_detector.parse()

            is_bot = device_detector.is_bot()

            device_type = (
                device_detector.device_type() if device_detector.device_type() else None
            )

            device_brand = (
                device_detector.device_brand()
                if device_detector.device_brand()
                else None
            )

            device_model = (
                device_detector.device_model()
                if device_detector.device_model()
                else None
            )

            os_name = device_detector.os_name() if device_detector.os_name() else None

            os_version = (
                device_detector.os_version() if device_detector.os_version() else None
            )

            return is_bot, device_type, device_brand, device_model, os_name, os_version

        except Exception as e:
            print("ERROR: Audit Login -> dump_user_agent: " + str(e))

        return None, None, None, None, None, None
