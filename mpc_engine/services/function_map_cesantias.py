from typing import Callable

from mpc_engine.services.queries import (
    get_official_info,
    get_request_info
)

# Diccionario parametrizable de funciones expuestas
function_map: dict[str, Callable] = {
    "buscar_funcionario_por_cedula": get_official_info,
    "ver_estado_solicitud": get_request_info,
}