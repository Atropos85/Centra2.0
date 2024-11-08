from django.urls import path
from views.utils import function_autocomplete, generate_pdf
from cesantias.views.request_views import RequestView, RequestListView, get_previous_severance_value_ajax

urlpatterns = [
    path('solicitudes/', RequestListView.as_view(), name='list_requests'),
    path('function_autocomplete/', function_autocomplete, name='function_autocomplete'),
    path('get_previous_severance_value_ajax/<int:number_ID>/',get_previous_severance_value_ajax, name='get_previous_severance_value_ajax'),
    path('solicitudes/create', RequestView.create_request, name='create_request'),
    path('solicitudes/edit/<int:request_id>/', RequestView.create_request, name='edit_request'),
    path('reporte/', generate_pdf, name='generate_pdf'),
]
