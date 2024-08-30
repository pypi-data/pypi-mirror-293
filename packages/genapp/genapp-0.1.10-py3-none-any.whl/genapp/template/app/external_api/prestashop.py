from app.external_api.connection.connection import Connection

# Ejemplo de uso:
#
#


class PrestashopKeys:
    PRODUCTS = "products"
    PRODUCTS_IMAGES = "images/products"
    CATEGORIES = "categories"
    CUSTOMERS = "customers"
    ORDERS = "orders"
    MANUFACTURERS = "manufacturers"
    SUPPLIERS = "suppliers"
    ATTRIBUTES = "atributtes"
    COMBINATIONS = "combinations"
    CARRIERS = "carriers"
    TAX_RULES = "tax_rules"
    CUSTOMERS_GROUPS = "customer_groups"
    LANGUAGES = "languages"
    CURRENCIES = "currencies"
    STORES = "stores"


class Prestashop(Connection):

    url = "http://localhost/prestashop/api"  # Url o dominio de la API

    api_key = "XXXX"

    async def get_data(self, funtionality):
        try:
            self.headers.update({"Authorization": f"Basic {self.api_key}"})

            self.path = funtionality

            response, _ = await self.get()

            if response.status_code == 200:
                return response.json()

        except Exception as e:
            print("ERROR: External Api Prestashop -> get_data: " + str(e))

        return None
