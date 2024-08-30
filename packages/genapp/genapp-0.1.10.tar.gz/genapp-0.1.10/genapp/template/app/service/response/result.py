class ResultCodes:
    NO_MORE_DATA = "000"
    DATA_AVAILABLE = "001"
    NO_DATA = "002"

    # CONFIGURATION
    # Exito
    CONFIGURATION_OK = "100"

    # Error
    CONFIGURATION_FAIL = "101"
    CONFIGURATION_USER_EXISTS = "102"
    CONFIGURATION_NOT_FTOKEN = "112"
    CONFIGURATION_UPDATE_FTOKEN_FAIL = "113"
    CONFIGURATION_INSERT_FTOKEN_FAIL = "114"
    CONFIGURATION_DEVICE_NOT_EXISTS = "121"

    # CALENDAR APPOINTMENTS

    ################  CALENDAR GENERIC ################
    # Error
    # Un usuario hace funcionalidad con fallo
    APPOINMENT_FAIL = "201"
    # Appointment existente
    APPOINTMENT_ALREADY_EXISTS = "202"
    # Appointment no disponible
    APPOINTMENT_NOT_AVAILABLE = "205"
    # Appointment falla al insertar
    APPOINTMENT_INSERT_FAIL = "204"
    # Un usuario hace una funcionalidad con appointment que no existe o no es accesible
    APPOINTMENT_NOT_EXISTS = "203"

    ################  CALENDAR EMPLOYEE ################
    # Exito
    # Empleado hace una funcionalidad con exito
    APPOINTMENT_OK_EMPLOYEE = "240"
    # Empleado hace funcionalidad con exito de un appointment no aceptada
    APPOINTMENT_WASNT_ACCEPTED_EMPLOYEE = "241"
    # Empleado hace funcionalidad con exito de un appointment aceptada
    APPOINTMENT_WAS_ACCEPTED_EMPLOYEE = "242"

    # Error
    # Empleado hace funcionalidad invalida
    APPOINTMENT_EMPLOYEE_NOT_VALID = "245"

    ################  CALENDAR CUSTOMER ################
    # Exito
    # Cliente hace una funcionalidad con exito
    APPOINTMENT_OK_CUSTOMER = "230"
    # Cliente hace funcionalidad con exito de un appointment no aceptada
    APPOINTMENT_WASNT_ACCEPTED_CUSTOMER = "231"
    # Cliente hace funcionalidad con exito de un appointment aceptada
    APPOINTMENT_WAS_ACCEPTED_CUSTOMER = "232"

    # Error
    # Cliente hace funcionalidad sin exito
    APPOINTMENT_CUSTOMER_NOK = "235"

    CODE_ERROR = [
        CONFIGURATION_FAIL,
        CONFIGURATION_USER_EXISTS,
        CONFIGURATION_NOT_FTOKEN,
        CONFIGURATION_UPDATE_FTOKEN_FAIL,
        CONFIGURATION_INSERT_FTOKEN_FAIL,
        CONFIGURATION_DEVICE_NOT_EXISTS,
        APPOINMENT_FAIL,
        APPOINTMENT_ALREADY_EXISTS,
        APPOINTMENT_NOT_AVAILABLE,
        APPOINTMENT_INSERT_FAIL,
        APPOINTMENT_NOT_EXISTS,
        APPOINTMENT_EMPLOYEE_NOT_VALID,
        APPOINTMENT_CUSTOMER_NOK,
    ]


class ResultAPI:

    def __init__(
        self,
        error: bool = False,
        has_next: bool = False,
        code: str = None,
        code_list: list = None,
    ):
        self.error = error

        if has_next:
            self.code = ResultCodes.DATA_AVAILABLE
        else:
            self.code = ResultCodes.NO_MORE_DATA

        if code_list:
            for code in code_list:
                if code:
                    self.code = code
                    if self.is_error(code):
                        self.error = True
                        break

        if code:
            self.code = code
            self.error = self.is_error(code)

    def is_error(self, code):
        return code in ResultCodes.CODE_ERROR
