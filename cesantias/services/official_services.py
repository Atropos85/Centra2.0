from ..models.official import Official, NoWorkDays
from ..forms.request_form import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

#@login_required
def official_autocomplete(request,search_term):

    officials = Official.objects.filter(number_ID__istartswith=search_term)[:10]  # Limitar el número de resultados
    results = []
    for official in officials:
        no_work_days = NoWorkDays.objects.filter(official_ID=official).first()  # Obtiene los días no laborables
        gender_dict = dict(Official.GENDER_CHOICES)
        results.append({
            'numid': official.number_ID,
            'text': f'({official.number_ID}) {official.names} {official.last_names}',
            'vnumber_id': official.number_ID,
            'vnames': official.names,
            'vlast_names': official.last_names,
            'vgender': gender_dict.get(official.gender, 'Desconocido'),  # Convierte el valor a su representación legible
            'ventity_id': official.entity_ID.entity_name,
            'vcity': official.city.city_name,
            'vdepartament': official.departament.depto_name,
            'vaddress': official.address,
            'vphone': official.phone,
            'vextensions': official.extensions,
            'vcelphone': official.celphone,
            'vstartdate': official.start_date.strftime('%d/%m/%Y'),
            'vno_work_days': no_work_days.no_work_days if no_work_days else 0  # Incluye los días no laborables si existen
        })

    return JsonResponse({'results': results})