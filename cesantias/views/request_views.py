from django.shortcuts import render, redirect
from ..models.request import Request,WageFactors,RequestDetail, Certifications
from ..forms.request_form import *
from ..services.request_service import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import ListView

class RequestListView(ListView):
    model = Request
    template_name = 'cesantias/request/list/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        qs = Request.objects.all().order_by('-update_date')
        
        # Aplica filtros si hay parámetros en GET
        self.filter = RequestFilter(self.request.GET, queryset=qs)
        
        # Devuelve los resultados filtrados o el queryset original
        return self.filter.qs[:15]  # Limita a los primeros 15 resultados

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_set, _ = get_all_requests(self.request)
        # Añadir el filtro al contexto para usar en la plantilla
        context['filters'] = filter_set
        return context
    
@login_required
class RequestView:
    @staticmethod
    def list_requests(request):
        requests = get_all_requests(request)
        return render(request, 'cesantias/request/list/request_list.html', {'requests': requests})

    @staticmethod
    def create_request(request, request_id=None):
        # Llamar al servicio que procesa el formulario
        response = RequestCreate.create_request_post(request, request_id)
        # Validar si el checkbox está marcado
        request_form, request_detail_form, wage_factors_form, cert_formset, official_form, visible_fields, history ,valid, request_ID=  response
        
        generate_report = request.POST.get('reporte_liquidacion')
        generate_cdp_report = request.POST.get('reporte_cdp')
        generate_rso_report = request.POST.get('reporte_Resolucion')
        generate_rpc_report = request.POST.get('reporte_rpc')        
        
        if request_id:
            if 'reports' not in request.session:   
                reports = RequestReport.update_state_from_report(request,request_id,generate_report,generate_cdp_report,generate_rso_report,generate_rpc_report)
                request.session['reports'] = reports
            else:
                reports = request.session.get('reports', None)
                del request.session['reports'] 
        else:
            reports= None

        if valid and (not request_id  or 'reports' in request.session):
            return redirect('edit_request', request_id=request_ID)
        else:
            if 'reports' in request.session:                
                del request.session['reports'] 
            
            # Renderizar el formulario con los errores si existen
            return render(request, 'cesantias/request/request_form.html', {
                'request_form': request_form,
                'request_detail_form': request_detail_form,
                'wage_factors_form': wage_factors_form,
                'certifications_formset': cert_formset,
                'official_form': official_form,                
                **visible_fields,
                'history': history,
                'reports':reports,
                })    

def get_previous_severance_value_ajax(request, number_ID):
    # Verifica si es una solicitud AJAX, pero sin bloquear la ejecución
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        history_list, total_filling_value = get_previous_severance_value(number_ID)
        history = [{'request_ID': hist.request_ID, 
                    'resolution_number': hist.resolution_number,
                    'resolution_date':hist.resolution_date,
                    'severance_disbursed_value':hist.severance_disbursed_value,
                    } for hist in history_list]
        return JsonResponse({
            'previous_severance_value': total_filling_value,
            'history': history
        })
    else:
        # Permitir que funcione aún si no es AJAX (por ejemplo, en pruebas en el navegador)
        history_list, total_filling_value = get_previous_severance_value(number_ID)
        history = [{'request_ID': hist.request_ID, 
                    'resolution_number': hist.resolution_number,
                    'resolution_date':hist.resolution_date,
                    'severance_disbursed_value':hist.severance_disbursed_value,
                    } for hist in history_list]
        return JsonResponse({
            'previous_severance_value': total_filling_value,
            'history': history
        })
    
def get_order_detail_response(request, template_name, context=None, **kwargs):
    CertificationsFormSet = modelformset_factory(Certifications, form=CertificationsForm, extra=2)

    context = context or {}
    # Agregar el formulario de oficial
    context['official_form'] = kwargs.get('official_form', OfficialForm())
    
    # Agregar el formulario de solicitud
    context['request_form'] = kwargs.get('request_form', RequestForm())
    
    # Agregar el formulario de certificación
    context['certification_formset'] = kwargs.get('certification_formset', CertificationsFormSet(queryset=Certifications.objects.none()))
    
    return render(request, template_name, context)
    