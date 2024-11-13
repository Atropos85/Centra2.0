from ..models.request import Request,WageFactors,RequestDetail, Certifications
from ..models.official import Official, NoWorkDays
from ..forms.request_form import *
from ..services.request_service import *
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
import json
from django.contrib import messages
from django.forms import modelformset_factory


@staticmethod
def get_all_requests(request):

    queryset = Request.objects.all().order_by('-update_date')

    # Crear el conjunto de filtros
    filter_set = RequestFilter(request.GET, queryset=queryset)

    if not any(value for value in request.GET.values() if value):
        # Si no hay filtros, limitar la consulta a los últimos 15 registros
        queryset = queryset[:15]

    # Devolver el conjunto de filtros y la queryset filtrada
    return filter_set, queryset

class RequestCreate:
 
    @staticmethod
    def create_request_post(request,request_id):
        if request_id:
            request_instance = get_object_or_404(Request, pk=request_id)
            request_detail_instance = request_instance.details.first() 
            wage_factors_instance = request_instance.wage_factors.first()  
            certifications = request_instance.certifications.all() 
            official_instance = request_instance.official_ID
            num_certifications = certifications.count() 
  
            history_list = get_request_history(request_id,official_instance.number_ID)
        else:
            request_instance = Request()
            request_detail_instance = RequestDetail()
            wage_factors_instance = WageFactors()
            official_instance = Official()
            certifications = Certifications.objects.none() 
            num_certifications = 0
            history_list = None

        history = history_list
        visible_fields = get_visible_fields(request_instance.request_state,
                                            request_instance.withdrawal_mode,
                                            request_id is None
                                           )
            
        max_certifications = 2  # Número máximo de certificaciones permitidas
        extra = max(0, max_certifications - num_certifications)  # Asegúrate de que no sea negativo
        CertificationsFormSet = modelformset_factory(Certifications, form=CertificationsForm, extra=extra)
   
        if request.method == 'POST':
            if request_id:
                official_form = OfficialForm(instance=official_instance)   
                requestActive = None   
            else:
                number_id = request.POST.get('number_ID')
                official_instance = Official.objects.filter(number_ID=number_id).first()
                official_form = OfficialForm(instance=official_instance)  

                requestActive = get_request_active(official_instance.official_ID )            

                if requestActive:
                    reqAct = requestActive.request_ID
                    messages.error(request, f'Existe una solicitud activa. Por favor validar la siguiente solicitud: {reqAct}')

            no_work_days_instance = NoWorkDays.objects.filter(official_ID=official_instance.official_ID).first()
            no_work_days_form = NoWorkDaysForm(request.POST or None, instance=no_work_days_instance)
            dias_no_trabajados = request.POST.get('no_work_days')

            request_form = RequestForm(request.POST, instance=request_instance)
            
            wage_factors_form = WageFactorsForm(request.POST, instance=wage_factors_instance)
            request_detail_form = RequestDetailForm(request.POST, instance=request_detail_instance)
            cert_formset = CertificationsFormSet(request.POST, queryset=certifications)

            if request_form.is_valid() and wage_factors_form.is_valid() and request_detail_form.is_valid() and cert_formset .is_valid() and requestActive == None:
               
                if request_form.has_changed():  # Solo guarda si hubo cambios en el formulario de solicitud
                    request_instance = request_form.save(commit=False)
                    request_instance.official_ID = official_instance
                    request_instance.save()

                for cert_form in cert_formset:
                    if cert_form.has_changed():  # Solo guarda si hubo cambios
                        certifications = cert_form.save(commit=False)
                        certifications.request = request_instance  # Asociar con la solicitud
                        certifications.save()

                # Verifica si alguna de las secciones visibles requiere guardar los detalles de la solicitud
                if any(visible_fields[field] for field in ['show_home_fields', 'show_def_fields', 'show_study_fields', 'show_hipo_fields']):
                    if request_detail_form.has_changed():  # Solo guarda si hubo cambios en el formulario de detalles
                        request_detail_instance = request_detail_form.save(commit=False)
                        request_detail_instance.request = request_instance
                        request_detail_instance.save()
                
                if dias_no_trabajados and int(dias_no_trabajados) != no_work_days_instance.no_work_days:
                    if no_work_days_form.is_valid():
                        no_work_days_instance = no_work_days_form.save(commit=False)
                        no_work_days_instance.request_ID = request_instance.request_ID
                        no_work_days_instance.no_work_days = dias_no_trabajados
                        no_work_days_instance.save()

                if wage_factors_form.has_changed():  # Solo guarda si hubo cambios en el formulario de factores salariales
                    wage_factors_instance = wage_factors_form.save(commit=False)
                    wage_factors_instance.request = request_instance  # Relacionar con la solicitud
                    wage_factors_instance.save()

                messages.success(request, 'Solicitud creada/actualizada con éxito.')
                valid = True
                request_ID = request_instance.pk
            else:              
                messages.error(request, 'Por favor corrige los errores en el formulario.')
                valid = False
                request_ID = None
        else:
            official_form = OfficialForm(instance=official_instance)
            request_form = RequestForm(instance=request_instance)
            request_detail_form = RequestDetailForm(instance = request_detail_instance )
            wage_factors_form = WageFactorsForm(instance=wage_factors_instance)
            cert_formset = CertificationsFormSet(queryset=certifications)
            valid = None
            request_ID = None
            
            
        return request_form, request_detail_form, wage_factors_form, cert_formset, official_form, visible_fields, history, valid, request_ID
    
def get_request_active(official_ID):
    request = Request.objects.filter(official_ID=official_ID,
                                     request_state__gte=1,
                                     request_state__lte=5
                                    ).first()   
    return request 

def get_request_history(request_ID,official_ID):
    # Filtra las solicitudes por estado y por el funcionario correspondiente
    official = get_object_or_404(Official, number_ID=official_ID)
    
    history = Request.objects.filter(
    official_ID=official,
    request_state__gte=5,
    request_state__lte=9
    )    
    
    if request_ID:
        request = get_object_or_404(Request, request_ID=request_ID)
        request_date =  request.request_date
        history = history.filter(request_date__lt = request_date)
    return history

def get_previous_severance_value(request_ID, number_ID):
    history = get_request_history(request_ID, number_ID)
    total_filling_value = history.aggregate(Sum('filling_value'))['filling_value__sum'] or 0
    return history, total_filling_value

def get_visible_fields(request_state, withdrawal_mode, is_new_request=False):
    # Inicializar un diccionario para mostrar los campos
    visibility = {
        'show_settlement_fields': False,
        'show_cdp_fields': False,

        'show_home_fields': False,
        'show_def_fields': False,
        'show_study_fields': False,
        'show_hipo_fields': False,
        'show_build_fields': False,

        'show_noti_fields': False,
        'show_fact_fields': False,
        'show_rpc_fields': False,
        'show_pago_fields': False,
    }

    # Solo valida si la solicitud no es nueva
    if not is_new_request:
        # Validar condiciones para los campos
        if request_state not in [1, 10]:
            visibility['show_settlement_fields'] = True

        if request_state not in [1, 2, 10]:
            visibility['show_cdp_fields'] = True
            # Determinar el modo de retiro
            if withdrawal_mode == 'V':
                visibility['show_home_fields'] = True
            elif withdrawal_mode == 'D':
                visibility['show_def_fields'] = True
            elif withdrawal_mode == 'E':
                visibility['show_study_fields'] = True
            elif withdrawal_mode == 'H':
                visibility['show_hipo_fields'] = True
            elif withdrawal_mode == 'R':
                visibility['show_build_fields'] = True

        if request_state not in [1, 2, 3, 10]:
            visibility['show_noti_fields'] = True

        if request_state not in [1, 2, 3, 4, 10]:
            visibility['show_fact_fields'] = True

        if request_state not in [1, 2, 3, 4, 5, 10]:
            visibility['show_rpc_fields'] = True

        if request_state not in [1, 2, 3, 4, 5, 6, 7, 10]:
            visibility['show_pago_fields'] = True
    return visibility
  

class RequestReport:
 
    def update_state_from_report(request,request_id,check_rep_liq,check_rep_cdp,check_rep_rso,check_rep_rpc):
        # Validar el estado de la solicitud
        reports = {
            'check_rep_liq': check_rep_liq,
            'check_rep_cdp': check_rep_cdp,
            'check_rep_rso': check_rep_rso,
            'check_rep_rpc': check_rep_rpc,
            'request_id'   : request_id,
        }

        #Se asignan los objetos
        try:
            req = Request.objects.get(request_ID=request_id) 
        except Request.DoesNotExist:
            req = Request()

        try:
            detail = RequestDetail.objects.get(request=request_id)
        except RequestDetail.DoesNotExist:
            detail = RequestDetail()

        try:
            wage = WageFactors.objects.get(request=request_id)
        except WageFactors.DoesNotExist:
            wage = WageFactors()                

        try:
            cert = Certifications.objects.filter(request=request_id)
            nucer = cert.count()
        except Certifications.DoesNotExist:
            cert = 0  

        #Se validan si se van a generar reportes
        if check_rep_liq or check_rep_cdp or check_rep_rso or check_rep_rpc: 
                
            if nucer == 0:  # Si no hay certificaciones
                messages.error(request, 'No es posible generar el reporte. No existe un registro de certificaciones asociado a la solicitud.')
                return None
            if not wage.pk:  # Si no hay una instancia de WageFactors
                messages.error(request, 'No es posible generar el reporte. No existe un registro de factores salariales asociado a la solicitud.')
                return None
            
            if check_rep_liq:
                reports['check_rep_liq'] = True
                if req.request_state == 1:   # RADICADA
                    req.request_state = 2  # Cambiar el estado a LIQUIDADA
                    req.settlement_date = timezone.now()  
                    req.save()

            if check_rep_cdp:
                reports['check_rep_cdp'] = True
                if req.request_state == 1 or req.request_state == 2:
                    req.request_state = 3  # Cambiar el estado a CPD SOLICITDO
                    req.cdp_request_date = timezone.now()
                    req.save() 

            if check_rep_rso:
                if req.cdp_issue_date and req.cdp_number and req.holder_position:
                    if ((req.withdrawal_mode == 'V' and detail.sell_seller and detail.sell_doc_type and detail.sell_doc_num)
                    or (req.withdrawal_mode == 'D' and detail.def_resolution and detail.def_date and detail.def_position)
                    or (req.withdrawal_mode == 'E' and detail.est_nit and detail.est_institution)
                    or (req.withdrawal_mode == 'H' and detail.hip_loan_number and detail.hip_nit and detail.hip_bank)
                    or (req.withdrawal_mode == 'R')
                    or (req.withdrawal_mode not in ['V', 'D', 'E', 'H', 'R'])):
                        reports['check_rep_rso'] = True
                        if req.request_state == 3:
                            req.request_state = 4  # Cambiar el estado a EMISION RESOLUCION
                            req.save()                         
                    else :
                        messages.error(request, 'No es posible crear el reporte.Por favor diligencie los campos asociados al tipo de retiro de cesantias.')
                        reports['check_rep_rso'] = False
                else :
                    messages.error(request, 'No es posible crear el reporte.Por favor diligencie los campos asociados al CDP.')
                    reports['check_rep_rso'] = False
                
            if check_rep_rpc:
                if req.notify_date and req.resolution_date and req.resolution_number:
                    reports['check_rep_rpc'] = True
                    if req.request_state == 4 or req.request_state == 5:
                        req.request_state = 6  # Cambiar el estado a RPC SOLICITADO
                        req.rpc_request_date = timezone.now()
                        req.save()                        
                else :
                    messages.error(request, 'No es posible crear el reporte.Por favor diligencie los campos asociados a la resolucion.')
                    reports['check_rep_rpc'] = False                

        #Se actualiza el estado validando campos
        if req.notify_date:
            if req.request_state == 4:
                req.request_state = 5  # Cambiar el estado a NOTIFICADO
                req.save() 

        if req.rpc_request_date and req.rpc_number:
            if req.request_state == 6:
                req.request_state = 7  # Cambiar el estado a RPC EMITIDO
                req.save() 

        if req.rpc_request_date and req.rpc_number:
            if req.request_state == 6 or req.request_state == 7:
                req.request_state = 8  # Cambiar el estado a PASO A FACTURACION
                req.save()   

        if req.billing_date and req.treasury_date and req.billing_number:
            if req.request_state == 8:
                req.request_state = 9  # Cambiar el estado a PROCESO DE PAGO
                req.save()   
        
        py_dict = json.dumps(reports)
        return py_dict