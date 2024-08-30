# Claves para el contenido de data
class DataKey:
    DATE_KEY = "date"
    DATE_KEYS_REPLACE = ["fecha", "fechasesion"]
    PERIOD_KEY = "period"
    PERIOD_KEYS_REPLACE = ["periodo", "hora"]
    ENERGY_MW_KEY = "energy_mw"
    ENERGY_MW_KEYS_REPLACE = ["energia"]
    ENERGY_KW_KEY = "energy_kw"
    ENERGY_KW_KEYS_REPLACE = ["energia_kw", "energia_disponibilidad", "e2"]


def format_data(data):
    try:
        if isinstance(data, list):
            for element in data:
                if isinstance(element, dict):
                    keys_to_replace = list(element.keys())

                    for key in keys_to_replace:
                        if key in DataKey.DATE_KEYS_REPLACE:
                            element[DataKey.DATE_KEY] = element[key]
                            element.pop(key)

                        if key in DataKey.PERIOD_KEYS_REPLACE:
                            element[DataKey.PERIOD_KEY] = element[key]
                            element.pop(key)

                        if key in DataKey.ENERGY_MW_KEYS_REPLACE:
                            element[DataKey.ENERGY_MW_KEY] = element[key]
                            element.pop(key)

                        if key in DataKey.ENERGY_KW_KEYS_REPLACE:
                            element[DataKey.ENERGY_KW_KEY] = element[key]
                            element.pop(key)
        return data

    except Exception as e:
        print("ERROR: Request -> format_data: " + str(e))
        return None
