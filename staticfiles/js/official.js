        $(document).ready(function() {
            var fieldMapping = {
                'vnumber_id': '#id_number_ID',
                'vnames': '#id_names',
                'vlast_names': '#id_last_names',
                'vgender': '#id_gender_display',
                'vaddress': '#id_address',
                'vphone': '#id_phone',
                'vextensions': '#id_extensions',
                'vcelphone': '#id_celphone',
                'vcity': '#id_city_display',
                'vdepartament': '#id_departament_display',
                'ventity_id': '#id_entity_ID_display',
                'vstartdate': '#id_start_date',
                'vno_work_days': '#id_no_work_days',
                'severancePrev':'#id_previous_severance_value'
            };

            // Llamada a la función de autocompletar con la lógica de limpiar y llenar campos
            autocomplete('#id_number_ID', '#autocomplete-results', 'official_autocomplete', fieldMapping, function() {
                clearFields('#id_number_ID');  // Utilizar la función genérica de limpiar campos
            });
            clearfieldOnload('#id_number_ID', function() {
                clearFields('#id_number_ID');
        
            });
        });
        
        