from urllib.parse import urljoin

import httpx


class Connection:
    GET = "get"
    POST = "post"

    # Constantes a definir en cada conexion
    url = None  # Url o dominio de la API
    path_login = None  # Path para obtener el token JWT
    credentials = {}  # Credenciales necesarias para obtener un token JWT
    headers = {}  # Headers necesarios para realizar una solicitud hacia una api externa
    api_key = None
    json_key_token = ""

    # Token JWT necesario para la autorizacion
    token_jwt = None
    path = None

    #############################################################
    ##################### REQUESTS HANDLERS #####################
    #############################################################

    # Solicitud GET
    async def get(self, attempts=3):
        try:
            if attempts <= 0:
                return None, None

            if self.credentials:
                if not self.token_jwt:
                    self.token_jwt = await self._getToken()

            response = await self._getRequest()

            if response:
                if self.credentials and response.status_code in [401, 403]:
                    self.token_jwt = None
                else:
                    return response, self.token_jwt

            return await self.get(attempts=attempts - 1)

        except Exception as e:
            print("ERROR: External Api Connection -> get: " + str(e))
            return e, None

    # Solicitud POST
    async def post(self, json, attempts=3):
        try:
            if attempts <= 0:
                return None, None

            if self.credentials:
                if not self.token_jwt:
                    self.token_jwt = await self._getToken()

            response = await self._postRequest(json)

            if response:
                if self.credentials and response.status_code in [401, 403]:
                    self.token_jwt = None
                else:
                    return response, self.token_jwt

            return await self.post(json, attemps=attempts - 1)

        except Exception as e:
            print("ERROR: External Api Connection -> post: " + str(e))
            return e, None

    # Devuelve respuestas a solicitudes tipo GET con o sin token JWT
    async def _getRequest(self):
        try:
            async with httpx.AsyncClient(verify=False) as client:
                uri = self._getUri()
                if self.token_jwt:
                    self.headers.update({"Authorization": f"Bearer {self.token_jwt}"})

                return await client.get(
                    uri, headers=self.headers, follow_redirects=True
                )

        except Exception as e:
            print("ERROR: External Api Connection -> getRequest: " + str(e))

        return None

    # Devuelve respuestas a solicitudes tipo POST con o sin token JWT
    async def _postRequest(self, json):
        try:
            async with httpx.AsyncClient(verify=False) as client:
                uri = self._getUri()
                if self.token_jwt:
                    self.headers.update({"Authorization": f"Bearer {self.token_jwt}"})
                    self.headers.update({"Content-Type": "application/json; UTF-8"})
                return await client.post(
                    uri, headers=self.headers, json=json, follow_redirects=True
                )

        except Exception as e:
            print("ERROR: External Api Connection -> getRequest: " + str(e))

        return None

    # Metodo de obtencion del token JWT, a definir en cada conexion
    async def _getToken(self):
        try:
            async with httpx.AsyncClient(verify=False) as client:
                auth_response = await client.post(
                    self.path_login, data=self.credentials, follow_redirects=True
                )
                print(auth_response.json().get(self.json_key_token))
                if auth_response.status_code == 200:
                    return auth_response.json().get(self.json_key_token)

        except Exception as e:
            print("ERROR: External Api Connection -> getToken: " + str(e))

        return None

    # Obtiene un endpoint dada la URL de un API y una query
    def _getUri(self):
        try:
            if self.path:
                return self.url + "/" + self.path

            return self.url

        except Exception as e:
            print("ERROR: External Api Connection -> getUri: " + str(e))

        return None
