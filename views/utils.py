from django.apps import apps
from cesantias.services.official_services import official_autocomplete
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from services import reports_services

services_map = {
    'official_autocomplete': official_autocomplete,
    # Puedes agregar más servicios aquí, por ejemplo:
    # 'request_autocomplete': request_autocomplete
}

#@login_required
def function_autocomplete(request):
    if 'q' in request.GET:
        search_term = request.GET.get('q')
        services = request.GET.get('service')
        service_function = services_map.get(services)
        
        results = service_function(request,search_term)  # Usa el servicio para obtener los resultadoss
        return results

    return JsonResponse({'results': []})
def generate_pdf(request):
    # Obtener parámetros de la solicitud GET
    report_name = request.GET.get('report_name')
    object_id = request.GET.get('object_id')
    

    # Validar que los parámetros no sean None
    if not object_id or not report_name:
        return HttpResponse("Faltan parámetros en la solicitud.", status=400)

    report_data = reports_services.get_report_data(report_name, object_id)
    # Renderizar el template HTML
    html_content = render_to_string(f'reports/{report_name}.html', report_data)

    # Convertir el HTML a PDF
    pdf = HTML(string=html_content).write_pdf()

    # Configurar la respuesta para que se descargue el archivo PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report_name}_{object_id}.pdf"'

    return response