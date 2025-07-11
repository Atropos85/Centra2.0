from cesantias.models.official import Official
from cesantias.models.request import Request
from asgiref.sync import sync_to_async
import os

base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# ==== Buscar funcionario por cédula ====
@sync_to_async
def get_official_info(cedula: str) -> dict:
    try:
        o = Official.objects.get(number_ID=cedula)
        return {
            "found": True,
            "cedula": o.number_ID,
            "nombre": f"{o.names} {o.last_names}"
        }
    except Official.DoesNotExist:
        return {"found": False, "cedula": cedula}
    
# ==== Consultar estado de solicitud de cesantías ====
@sync_to_async
def get_request_info(cedula: str) -> dict:
    qs = Request.objects.filter(official_ID__number_ID=cedula).order_by("-request_date")
    
    if not qs.exists():
        return {
            "has_request": False,
            "mensaje": "No se encontraron solicitudes activas.",
            "url_crear": f"{base_url}/cesantias/solicitudes/create",
            "link_html": f'<a href="{f"{base_url}/cesantias/solicitudes/create"}" target="_blank">Editar Solicitud</a>',
             "link_markdown": f"[Editar Solicitud]({f"{base_url}/cesantias/solicitudes/create"})"
        
        }

    solicitud = qs.first()

    if solicitud.request_state == 1:  # Suponiendo que 1 = En edición
        campos_requeridos = {
            "cutoff_date": solicitud.cutoff_date,
            "filling_number": solicitud.filling_number,
            "filling_value": solicitud.filling_value,
            "severance_type": solicitud.severance_type,
            "withdrawal_mode": solicitud.withdrawal_mode,
            "no_work_days": solicitud.no_work_days,
        }
    else:
        campos_requeridos = {
            "cutoff_date": solicitud.cutoff_date,
            "filling_number": solicitud.filling_number,
            "filling_value": solicitud.filling_value,
            "severance_type": solicitud.severance_type,
            "withdrawal_mode": solicitud.withdrawal_mode,
            "no_work_days": solicitud.no_work_days,
        }

    campos_faltantes = [campo for campo, valor in campos_requeridos.items() if not valor]

    return {
        "has_request": True,
        "numero": solicitud.request_ID,
        "estado": solicitud.get_request_state_display(),
        "campos_faltantes": campos_faltantes,
        "url_editar": f"{base_url}/cesantias/solicitudes/edit/{solicitud.request_ID}/",
        "link_html": f'<a href="{f"{base_url}/cesantias/solicitudes/edit/{solicitud.request_ID}/"}" target="_blank">Editar Solicitud</a>',
        "link_markdown": f"[Editar Solicitud]({f"{base_url}/cesantias/solicitudes/edit/{solicitud.request_ID}/"})"
    }