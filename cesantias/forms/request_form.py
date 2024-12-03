from django import forms
from ..models.request import Request, WageFactors, Certifications, RequestDetail
from ..models.official import NoWorkDays, Official, City, Departament
from ..models.entities import Entities
import django_filters
from django.db.models import Value
from django.db.models.functions import Concat

class EntitiesForm(forms.ModelForm):
    class Meta:
        model = Entities
        fields = [
            'nick_name',
            'entity_name',
            'fund',
            'posPre',
            'ledger_account',
            'heading',
        ]

        widgets = {
            'nick_name': forms.TextInput(attrs={'placeholder': 'Sigla de la entidad'}),
            'entity_name': forms.TextInput(attrs={'placeholder': 'Nombre de la entidad'}),
            'fund': forms.TextInput(attrs={'placeholder': 'Fondo'}),
            'posPre': forms.TextInput(attrs={'placeholder': 'Código PosPre'}),
            'ledger_account': forms.NumberInput(attrs={'placeholder': 'Cuenta mayor'}),
            'heading': forms.TextInput(attrs={'placeholder': 'Rubro'}),
        }

class DepartamentForm(forms.ModelForm):
    class Meta:
        model = Departament
        fields = [
            'departament',
            'depto_name',
        ]   
        
class CityForm(forms.ModelForm):
    depto = DepartamentForm()
    class Meta:
        model = City
        fields = [
            'departament',
            'city',
            'city_name',
        ]        

class NoWorkDaysForm(forms.ModelForm):
    class Meta:
        model = NoWorkDays
        fields = [
            'official_ID',
            'no_work_days',
            'request_ID',
        ]

        widgets = {
            'no_work_days': forms.NumberInput(attrs={'placeholder': 'Número de días no trabajados'}),
            'request_ID': forms.NumberInput(attrs={'placeholder': 'Identificador de la solicitud'}),
        }

    def clean_no_work_days(self):
        no_work_days = self.cleaned_data.get('no_work_days')
        if no_work_days < 0:
            raise forms.ValidationError("El número de días no trabajados no puede ser negativo.")
        return no_work_days

class OfficialForm(forms.ModelForm):
    no_work_days = NoWorkDaysForm()
    entities = EntitiesForm()
    depto = DepartamentForm()
    city = CityForm()

    class Meta:
        model = Official
        fields = [
            'number_ID',
            'names',
            'last_names',
            'gender',
            'entity_ID',
            'city',
            'departament',
            'address',
            'phone',
            'extensions',
            'celphone',
            'start_date',
        ]
        
        widgets = {
            'number_ID': forms.TextInput(),
            'names': forms.TextInput(attrs={'disabled': 'disabled'}),
            'last_names': forms.TextInput(attrs={'disabled': 'disabled'}),
            'city': forms.TextInput(attrs={'disabled': 'disabled'}),
            'departament': forms.TextInput(attrs={'disabled': 'disabled'}),
            'address': forms.TextInput(attrs={'disabled': 'disabled'}),
            'phone': forms.TextInput(attrs={'disabled': 'disabled'}),
            'extensions': forms.TextInput(attrs={'disabled': 'disabled'}),
            'celphone': forms.TextInput(attrs={'disabled': 'disabled'}),
            'start_date': forms.DateInput(format='%d/%m/%Y',attrs={'disabled': 'disabled'}),            
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['names'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        self.fields['last_names'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        self.fields['address'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        self.fields['phone'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        self.fields['extensions'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        self.fields['celphone'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        self.fields['start_date'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        if self.instance.pk:  # Solo si ya existe una instancia
            # Agregar un campo solo lectura para mostrar la entidad
            
            self.fields['city_display'] = forms.CharField(
                initial=str(self.instance.city),  # Mostrar el nombre u otro campo que quieras
                disabled=True,
                label="Municipio",
            )

            self.fields['departament_display'] = forms.CharField(
                initial=str(self.instance.departament),  # Mostrar el nombre u otro campo que quieras
                disabled=True,
                label="Departamento"
            )

            self.fields['entity_ID_display'] = forms.CharField(
                initial=str(self.instance.entity_ID),  # Mostrar el nombre u otro campo que quieras
                disabled=True,
                label="Entidad"
            )
            
            gender_display = dict(self.Meta.model.GENDER_CHOICES).get(self.instance.gender, 'Desconocido')
            self.fields['gender_display'] = forms.CharField(
                initial=gender_display,  # Muestra la representación del género
                disabled=True,
                label="Género"
            )
        else:
            # Definir los campos para ser llenados dinámicamente con JavaScript
            self.fields['city_display'] = forms.CharField(
                initial='',  # Sin valor inicial
                disabled=True,
                label="Municipio",
                widget=forms.TextInput(attrs={
                    'class': 'clearable-field',  # Añadir las clases necesarias
                    'data-block': '1'
                })
            )
            self.fields['departament_display'] = forms.CharField(
                initial='',  
                disabled=True,
                label="Departamento",
                widget=forms.TextInput(attrs={
                    'class': 'clearable-field',  # Añadir las clases necesarias
                    'data-block': '1'
                })
            )
            self.fields['entity_ID_display'] = forms.CharField(
                initial='', 
                disabled=True,
                label="Entidad",
                widget=forms.TextInput(attrs={
                    'class': 'clearable-field',  # Añadir las clases necesarias
                    'data-block': '1'
                })
            )
            self.fields['gender_display'] = forms.CharField(
                initial='',  
                disabled=True,
                label="Género",
                widget=forms.TextInput(attrs={
                    'class': 'clearable-field',  # Añadir las clases necesarias
                    'data-block': '1'
                })
            )
            
        # Para que se muestren en el formulario, agrega estos campos a `self.base_fields`
        self.base_fields['city_display'] = self.fields['city_display']
        self.base_fields['departament_display'] = self.fields['departament_display']
        self.base_fields['entity_ID_display'] = self.fields['entity_ID_display']
        self.base_fields['gender_display'] = self.fields['gender_display']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("El teléfono solo puede contener números.")
        return phone

    def clean_celphone(self):
        celphone = self.cleaned_data.get('celphone')
        if celphone and not celphone.isdigit():
            raise forms.ValidationError("El celular solo puede contener números.")
        return celphone

class WageFactorsForm(forms.ModelForm):
    class Meta:
        model = WageFactors
        fields = [
            'wage', 
            'overwage', 
            'annual_bonus', 
            'holiday_bonus', 
            'christmas_bonus', 
            'bonus', 
            'transport_subsidy', 
            'food_subsidy', 
            'technical_bonus', 
            'seniority_bonus', 
            'accommodation_bonus', 
            'overtime', 
            'dev_by_draw', 
            'travel_expenses'
        ]
        widgets = {

            'wage': forms.TextInput(attrs={'placeholder': '0', 'onkeypress': 'return isNumberKey(event)',}),
            'overwage': forms.TextInput(attrs={'placeholder': '0', 'onkeypress': 'return isNumberKey(event)',}),
            'annual_bonus': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),
            'holiday_bonus': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),
            'christmas_bonus': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),
            'bonus': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}), 
            'transport_subsidy': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}), 
            'food_subsidy': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}), 
            'technical_bonus': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}), 
            'seniority_bonus': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),
            'accommodation_bonus': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),
            'overtime': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),
            'dev_by_draw': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),
            'travel_expenses': forms.TextInput(attrs={'placeholder': '0', 'step': '0.01','onkeypress': 'return isNumberKey(event)',}),           
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadir atributos a cada campo
        self.fields['wage'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['overwage'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['annual_bonus'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['holiday_bonus'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['christmas_bonus'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['bonus'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['transport_subsidy'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['food_subsidy'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['technical_bonus'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['seniority_bonus'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['accommodation_bonus'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['overtime'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['dev_by_draw'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['travel_expenses'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

class CertificationsForm(forms.ModelForm):
    class Meta:
        model = Certifications
        fields = [
            'request',
            'cert_date',
            'cert_number',
            'cert_name',
            'cert_position',
            'cert_entity_name',
        ]

        widgets = {
            'request':forms.HiddenInput(),
            'cert_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha', }),
            'cert_number': forms.TextInput(attrs={'placeholder': 'Ingrese el numero de la certificacion','onkeypress': 'return isNumberKey(event)',}),
            'cert_name': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de quien certifica','onkeypress': 'return isCharKey(event)',}),
            'cert_position': forms.TextInput(attrs={'placeholder': 'Ingrese el cargo de la persona que certifica','onkeypress': 'return isCharKey(event)',}),
            'cert_entity_name': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la entidad que certifica','onkeypress': 'return isCharKey(event)',}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadir atributos a cada campo
        self.fields['cert_date'].widget.attrs.update({
            'class': 'clearable-field form-control datepicker', 
            'data-block': '2'
        })

        self.fields['cert_number'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })  

        self.fields['cert_name'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['cert_position'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })  

        self.fields['cert_entity_name'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })        

class RequestDetailForm(forms.ModelForm):
    class Meta:
        model = RequestDetail
        fields = [
            'request',
            'sell_seller',
            'sell_doc_type',
            'sell_doc_num',
            'def_resolution',
            'def_date',
            'def_position',
            'est_nit',
            'est_institution',
            'hip_loan_number',
            'hip_nit',
            'hip_bank',
        ]

        widgets = {
            'request':forms.HiddenInput(), 
            'sell_seller': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del vendedor','onkeypress': 'return isCharKey(event)',}),
            'sell_doc_type': forms.TextInput(attrs={'placeholder': 'Ingrese el tipo de documento', 'onkeypress': 'return isCharKey(event)',}),
            'sell_doc_num': forms.TextInput(attrs={'placeholder': 'Ingrese el numero de documento','onkeypress': 'return isNumberKey(event)',}),

            'def_resolution' : forms.TextInput(attrs={'placeholder': 'Ingrese el numero de resolucion','onkeypress': 'return isNumberKey(event)', }),
            'def_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha', }),
            'def_position': forms.TextInput(attrs={'placeholder': 'Ingrese el cargo que certifica', 'onkeypress': 'return isCharKey(event)',}),

            'est_nit' : forms.TextInput(attrs={'placeholder': 'Ingrese el numero del NIT','onkeypress': 'return isNumberKey(event)', }),
            'est_institution': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la institucion','onkeypress': 'return isCharKey(event)', }),

            'hip_loan_number' : forms.TextInput(attrs={'placeholder': 'Ingrese el numero del prestamo','onkeypress': 'return isNumberKey(event)', }),
            'hip_nit' : forms.TextInput(attrs={'placeholder': 'Ingrese el numero del NIT','onkeypress': 'return isNumberKey(event)', }),
            'hip_bank': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del banco','onkeypress': 'return isCharKey(event)', }),
        }
        

class RequestForm(forms.ModelForm):
    class Meta:
        request_detail = RequestDetailForm()
        wage_factors = WageFactorsForm()
        certifications = CertificationsForm()

        official = OfficialForm()
        
        model = Request
        fields = [
            'official_ID',
            'request_date',
            'cutoff_date',
            'request_state',
            'filling_number',
            'filling_value',
            'severance_type',
            'withdrawal_mode',
            'total_days',
            'no_work_days',
            'working_days',
            'average_salary',
            'total_severance_value',
            'previous_severance_value',
            'balance_severance',
            'severance_disbursed_value',
            'settlement_date',
            'cdp_request_date',
            'cdp_issue_date',
            'cdp_number',
            'holder_position',
            'incharge_position',
            'notify_date',
            'resolution_date',
            'resolution_number',
            'rpc_request_date',
            'rpc_number',
            'billing_date',
            'treasury_date',
            'billing_number',
            'rejection_reason',
        ]

        widgets = {
            #Request
            'official_ID':forms.HiddenInput(),

            'request_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha',}),
            'cutoff_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha',}),
            'filling_number':forms.TextInput(attrs={'placeholder': 'Ingrese el numero de radicado','step': '0.01', 'onkeypress': 'return isNumberKey(event)',}),
            'filling_value': forms.TextInput(attrs={'placeholder': 'Ingrese el valor de la solicitud', 'onkeypress': 'return isNumberKey(event)',}),            
            #workindays
            'no_work_days' : forms.TextInput(attrs={'placeholder': '0','onkeypress': 'return isNumberKey(event)', }),
            'total_days' : forms.TextInput(attrs={'placeholder': '0','onkeypress': 'return isNumberKey(event)', 'readonly': 'readonly'}),
            'working_days' : forms.TextInput(attrs={'placeholder': '0','onkeypress': 'return isNumberKey(event)', 'readonly': 'readonly'}),
            #Liquidacion
            'settlement_date': forms.DateInput(format='%d/%m/%Y',attrs={'placeholder': 'Escoja fecha', 'readonly': 'readonly' }),
            'cdp_request_date': forms.DateInput(format='%d/%m/%Y',attrs={'placeholder': 'Escoja fecha', 'readonly': 'readonly' }),
            #CDP
            'cdp_issue_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha', }),
            'cdp_number': forms.TextInput(attrs={'placeholder': 'Ingrese el numero del CDP', 'step': '0.01', 'onkeypress': 'return isNumberKey(event)',}),
            'holder_position': forms.TextInput(attrs={'placeholder': 'Ingrese el cargo de la persona',}),
            'incharge_position': forms.TextInput(attrs={'placeholder': 'Ingrese el cargo encargado',}), 
            #Emision Resolucion
            'notify_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha' }),
            'resolution_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha', }),
            'resolution_number': forms.TextInput(attrs={'placeholder': 'Ingrese el numero de la resolucion','step': '0.01',}),
            #Proceso de Pago
            'rpc_request_date': forms.DateInput(format='%d/%m/%Y',attrs={'placeholder': 'Escoja fecha', 'readonly': 'readonly'  }),
            'rpc_number': forms.TextInput(attrs={'placeholder': 'Ingrese el numero del RPC','step': '0.01', 'onkeypress': 'return isNumberKey(event)',}),
            'treasury_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha', }),
            'billing_date': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker','placeholder': 'Escoja fecha', }),   
            'billing_number': forms.TextInput(attrs={'placeholder': 'Ingrese el numero de la factura','step': '0.01', 'onkeypress': 'return isNumberKey(event)',}),
            #Pago cesantias
            'average_salary': forms.TextInput(attrs={'placeholder': '0','step': '0.01', 'onkeypress': 'return isNumberKey(event)','readonly': 'readonly'}),
            'total_severance_value': forms.TextInput(attrs={'placeholder': '0','step': '0.01', 'onkeypress': 'return isNumberKey(event)','readonly': 'readonly'}),
            'previous_severance_value': forms.TextInput(attrs={'placeholder': '0','step': '0.01', 'onkeypress': 'return isNumberKey(event)','readonly': 'readonly'}),
            'balance_severance': forms.TextInput(attrs={'placeholder': '0','step': '0.01', 'onkeypress': 'return isNumberKey(event)','readonly': 'readonly'}),
            'severance_disbursed_value': forms.TextInput(attrs={'placeholder': '0','step': '0.01', 'onkeypress': 'return isNumberKey(event)','readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadir atributos a cada campo
        self.fields['request_date'].widget.attrs.update({
            'class': 'clearable-field form-control datepicker', 
            'data-block': '2'
        })

        # Añadir atributos a cada campo
        self.fields['cutoff_date'].widget.attrs.update({
            'class': 'clearable-field form-control datepicker', 
            'data-block': '2'
        })

        self.fields['filling_number'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['filling_value'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['severance_type'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['withdrawal_mode'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['filling_value'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['severance_type'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['withdrawal_mode'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['no_work_days'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '2'
        })

        self.fields['total_days'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        })

        self.fields['working_days'].widget.attrs.update({
            'class': 'clearable-field', 
            'data-block': '1'
        }) 

class RequestFilter(django_filters.FilterSet):
    request_ID = django_filters.CharFilter(lookup_expr='icontains', widget=forms.NumberInput(attrs={'style': 'width: 50px;'}))
    official_ID_number_ID = django_filters.CharFilter(field_name='official_ID__number_ID', lookup_expr='icontains',widget=forms.TextInput(attrs={ 'style': 'width: 100px;'}))
    official_ID_name = django_filters.CharFilter(method='filter_by_full_name', widget=forms.TextInput(attrs={ 'style': 'width: 300px;'}))

    request_date = django_filters.DateFilter(lookup_expr='exact' , widget=forms.DateInput(attrs={'class': 'datepicker'}))
    filling_number = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'style': 'width: 50px;'}))
    filling_value = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'style': 'width: 50px;'}))
    class Meta:
        model = Request
        fields = {
            'request_ID': ['icontains'],  # Filtrar por ID exacto o que contenga el valor
            'request_date': ['exact'],  # Filtrar por fecha exacta, antes o después
            'request_state': ['exact'],            # Filtrar por estado exacto
            'filling_number': ['icontains'],  # Filtrar por fecha exacta, antes o después
            'filling_value': ['icontains'],            # Filtrar por estado exacto
            'withdrawal_mode':['exact'], 
        }

    def filter_by_full_name(self, queryset, name, value):
        # Anotación para concatenar los nombres y apellidos

        queryset = queryset.annotate(
            full_name=Concat('official_ID__names', Value(' '), 'official_ID__last_names')
        )
        # Filtro por el campo concatenado
        return queryset.filter(full_name__icontains=value)