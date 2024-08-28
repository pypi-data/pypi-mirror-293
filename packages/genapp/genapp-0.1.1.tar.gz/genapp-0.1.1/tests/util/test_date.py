import pytest
import datetime

from app.util import date as Dt


# # Casos de prueba
# @pytest.mark.parametrize(
#     "input_date, expected_output",
#     [
#         (
#             datetime(2024, 5, 15),
#             "2024-05-15",
#         ),  # Caso de prueba para datetime_to_str con una fecha válida
#         (
#             "2024-05-15",
#             datetime(2024, 5, 15),
#         ),  # Caso de prueba para str_to_datetime con una cadena válida
#         (
#             "2024-05-15",
#             datetime(2024, 5, 15, 0, 0, 0),
#         ),  # Caso de prueba para str_to_day_init_datetime con una cadena válida
#     ],
# )
# def test_valid_inputs(input_date, expected_output):
#     # Verificar la función datetime_to_str
#     if isinstance(input_date, datetime):
#         assert Dt.datetime_to_str(input_date) == expected_output

#     # Verificar la función str_to_datetime
#     if isinstance(expected_output, datetime):
#         assert Dt.str_to_datetime(input_date) == expected_output

#     # Verificar la función str_to_day_init_datetime
#     if isinstance(expected_output, datetime):
#         assert Dt.str_to_day_init_datetime(input_date) == expected_output


# @pytest.mark.parametrize(
#     "invalid_input",
#     [
#         "2024-15-15",  # Caso de prueba para str_to_datetime con una cadena inválida
#         "2024-15-15",  # Caso de prueba para str_to_day_init_datetime con una cadena inválida
#     ],
# )
# def test_invalid_inputs(invalid_input):
#     # Verificar que str_to_datetime genere una excepción con una cadena inválida
#     with pytest.raises(Exception):
#         Dt.str_to_datetime(invalid_input)

#     # Verificar que str_to_day_init_datetime genere una excepción con una cadena inválida
#     with pytest.raises(Exception):
#         Dt.str_to_day_init_datetime(invalid_input)
