from app.util import object as Obj
from app.util import string as St
from app.service import cache as Cache
from app.service.request.request import Request


class ProxyAPI(Request):
    POST = "post"
    GET = "get"

    token = None
    path = None

    def __init__(self, funtionality, path):
        try:
            # Nombre de la funcionalidad y del modulo.py que se tiene que importar
            self.funtionality_name = funtionality
            self.path = path

            self.token = Cache.get_extenal_api_token(self.funtionality_name)

        except Exception as e:
            print("ERROR: Proxy api -> init: " + str(e))
            self.return_server_error()

    async def get(self):
        external_api = self._instance_external_api()

        response, token_jwt = await getattr(external_api, self.GET)()

        if isinstance(response, Exception):
            self.return_bad_gateway()

        if token_jwt:
            Cache.update_extenal_api_token(self.funtionality_name, token_jwt)

        if isinstance(response, bool) and response:
            self.response_ok()

        elif not isinstance(response, bool) and response:
            return response.json()

        self.return_server_error()

    async def post(self, json):
        external_api = self._instance_external_api()

        if json:
            response, token_jwt = await getattr(external_api, self.POST)(json)

            if isinstance(response, Exception):
                self.return_bad_gateway()

            if token_jwt:
                Cache.update_extenal_api_token(self.funtionality_name, token_jwt)

            if isinstance(response, bool) and response:
                self.response_ok()
            elif not isinstance(response, bool) and response:
                return response.json()
        else:
            self.response_error()

        self.return_server_error()

    # Instancia un objecto external api
    def _instance_external_api(self):
        try:
            return Obj.instance_external_api(
                self.funtionality_name, params=(self.token, self.path)
            )

        except Exception as e:
            print("ERROR: Proxy api -> instance_external_api: " + str(e))

        self.return_server_error()
