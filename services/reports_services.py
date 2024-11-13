from cesantias.models.request import  *
from cesantias.services.request_service import get_previous_severance_value
from num2words import num2words

def get_data_for_request_report(object_id):
    # Obtener la información relacionada para el reporte de Liquidación
    request = Request.objects.get(pk=object_id)
    request_detail = RequestDetail.objects.filter(request=object_id).first()
    wage_factors = WageFactors.objects.filter(request=object_id).first()
    certification = Certifications.objects.filter(request=object_id).first() 

    history_queryset, total_value = get_previous_severance_value(request.request_ID,request.official_ID.number_ID)
        
    valor_numerico = int(request.severance_disbursed_value)
    valor_en_letras = num2words(valor_numerico, lang='es').upper() if isinstance(valor_numerico, (int, float)) else ''
    
    return {'request': request,
            'request_detail': request_detail,
            'wage_factors': wage_factors,
            'certification': certification,
            'history': history_queryset,
            'valor_en_letras': valor_en_letras,
    }

# Función genérica para obtener los datos según el tipo de reporte
def get_report_data(report_name, object_id):
    if report_name == 'Liquidacion' or report_name == 'Solicitud_CDP' or report_name == 'Solicitud_RPC' or report_name == 'Emision_Resolucion':
        return get_data_for_request_report(object_id)
    else:
        raise ValueError("Nombre de reporte no válido.")
