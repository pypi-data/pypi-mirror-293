from app.external_api.connection.connection import Connection

# Ejemplo de uso:
#
#    https://api.ipgeolocation.io/ipgeo?apiKey=725e8bde9dcb448fa340ba160c028ed2&ip=194.224.31.74


class IpGeoKeys:
    IP = "ip"
    CONTINENT_CODE = "continent_code"
    CONTINENT_NAME = "continent_name"
    COUNTRY_CODE2 = "country_code2"
    COUNTRY_CODE3 = "country_code3"
    COUNTRY_NAME = "country_name"
    COUNTRY_NAME_OFFICIAL = "country_name_official"
    COUNTRY_CAPITAL = "country_capital"
    REGION = "state_prov"
    STATE_CODE = "state_code"
    DISTRICT = "district"
    CITY = "city"
    ZIPCODE = "zipcode"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    IS_EU = "is_eu"
    CALLING_CODE = "calling_code"
    COUNTRY_TLD = "country_tld"
    LANGUAGES = "languages"
    COUNTRY_FLAG = "country_flag"
    GEONAME_ID = "geoname_id"
    ISP = "isp"


class IpGeo(Connection):
    LOCALHOST = "127.0.0.1"

    # Funcionalidades
    ip_geo_funtionality = "ipgeo?"

    # Keys de parametros por GET
    api_key_parameter = "apiKey="
    ip_parameter = "ip="

    url = "https://api.ipgeolocation.io"  # Url o dominio de la API

    api_key = "725e8bde9dcb448fa340ba160c028ed2"

    async def get_data(self, ip):
        try:
            if ip != self.LOCALHOST:
                self.path = (
                    self.ip_geo_funtionality
                    + self.api_key_parameter
                    + str(self.api_key)
                    + "&"
                    + self.ip_parameter
                    + str(ip)
                )
                response, _ = await self.get()
                if response:
                    return response.json()
        except Exception as e:
            print("ERROR: External Api IpGeo -> get_data: " + str(e))

        return None


"""
{
'ip': '194.224.31.74',
'continent_code': 'EU',
'continent_name': 'Europe',
'country_code2': 'ES',
'country_code3': 'ESP',
'country_name': 'Spain',
'country_name_official': 'Kingdom of Spain',
'country_capital': 'Madrid',
'state_prov': 'Aragon',
'state_code': 'ES-AR',
'district': '',
'city': 'Zaragoza',
'zipcode': '50001', 'latitude': '41.65064',
'longitude': '-0.88210', 'is_eu': True,
'calling_code': '+34', 'country_tld': '.es'
, 'languages': 'es-ES,ca,gl,eu,oc',
'country_flag': 'https://ipgeolocation.io/static/flags/es_64.png',
'geoname_id': '6513785',
'isp': 'TDENET (Red de servicios IP)',
'connection_type': '',
'organization': 'TDENET (Red de servicios IP)',
'country_emoji': '🇪🇸',
'currency': {
    'code': 'EUR',
    'name': 'Euro',
    'symbol': '€'
},
'time_zone': {
    'name': 'Europe/Madrid',
    'offset': 1,
    'offset_with_dst': 2,
    'current_time': '2024-04-09 11:23:52.484+0200',
    'current_time_unix': 1712654632.484,
    'is_dst': True,
    'dst_savings': 1,
    'dst_exists': True,
    'dst_start': {
        'utc_time': '2024-03-31 TIME 01',
        'duration': '+1H',
        'gap': True,
        'dateTimeAfter': '2024-03-31 TIME 03',
        'dateTimeBefore': '2024-03-31 TIME 02',
        'overlap': False
    },
    'dst_end': {
        'utc_time': '2024-10-27 TIME 01',
        'duration': '-1H',
        'gap': False,
        'dateTimeAfter': '2024-10-27 TIME 02',
        'dateTimeBefore': '2024-10-27 TIME 03',
        'overlap': True}
    }
}
"""
