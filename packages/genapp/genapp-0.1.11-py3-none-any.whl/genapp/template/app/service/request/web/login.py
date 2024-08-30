from app.service.request.request_view import RequestView


class Login(RequestView):
    """
    Ejemplo content = {'cod_uf': ['ATALAYA'], 'fecha_inicio': ['2024-03-27'], 'fecha_fin': ['2024-03-28']}

    """

    async def post(self, user, content):
        # Obtener el método dinámico basado el contenido de funtionality
        pass

    async def get(self, user, content):
        try:
            return self.render("login")

        except ValueError or TypeError or IndexError as e:
            print("ERROR: Login -> get: " + str(e))

    async def xlogin(self, user, content):
        try:
            return None, None

        except Exception as e:
            print("ERROR: Login -> xlogin: " + str(e))

        return None, None
