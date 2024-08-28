from app.service.request.request_view import RequestView
from app.service.request.funtionality.configuration import Configuration


class SignUp(RequestView):
    """
    Ejemplo content = {'cod_uf': ['ATALAYA'], 'fecha_inicio': ['2024-03-27'], 'fecha_fin': ['2024-03-28']}

    """

    async def post(self, user, content):
        result_code, _ = await Configuration(None, None).xsign_up(None, content)
        # Obtener el método dinámico basado el contenido de funtionality
        return result_code

    async def get(self, user, content):
        try:
            return self.render("sign_up")

        except ValueError or TypeError or IndexError as e:
            print("ERROR: SignUp -> get: " + str(e))

    async def xsign_up(self, user, content):
        try:
            return None, None

        except Exception as e:
            print("ERROR: SignUp -> xsign_up: " + str(e))

        return None, None
