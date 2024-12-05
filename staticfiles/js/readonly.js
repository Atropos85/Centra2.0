document.addEventListener('DOMContentLoaded', function() {
    // Obtener el valor de request_state
    const requestStateValue = document.getElementById('requestStateValue').value;
    const withdrawalModeSelect = document.getElementById('id_withdrawal_mode');


    // Estados RADICADA  Y LIQUIDADA Y CDP SOLICITADO PERMITEN ACTUALIZAR LA INFORMACION DE LA SOLICITUD
    if (!requestStateValue || !['1','2','3'].includes(requestStateValue)) {
        // Obtener los elementos del formulario
        const filling_numInput = document.getElementById('id_filling_number');
        const filling_valInput = document.getElementById('id_filling_value');
        const request_dateInput = document.getElementById('id_request_date'); // DatePicker
        const cutoff_dateInput = document.getElementById('id_cutoff_date'); // DatePicker 
        const severance_Input = document.getElementById('id_severance_type'); // Select
        const withdrawal_Input = document.getElementById('id_withdrawal_mode'); // Select

        filling_numInput.setAttribute('readonly', true)
        filling_valInput.setAttribute('readonly', true)
        request_dateInput.setAttribute('readonly', true)
        cutoff_dateInput.setAttribute('readonly', true)
        severance_Input.setAttribute('readonly', true)
        withdrawal_Input.setAttribute('readonly', true)

        // Bloquear los selects para que no sean editables
        if (severance_Input) {
            severance_Input.addEventListener('mousedown', function(event) {
                event.preventDefault(); // Evita que se abra el menú desplegable
            });
        }

        if (withdrawal_Input) {
            withdrawal_Input.addEventListener('mousedown', function(event) {
                event.preventDefault(); // Evita que se abra el menú desplegable
            });
        }
    }
    // Estados CDP SOLICITADO  Y SOLICITUD RESOLUCION PERMITE ACTUALIZAR LA INFORMACION DEL CDP  
    if (!requestStateValue || !['1','2','3','4'].includes(requestStateValue)) {
        const cdp_dateInput = document.getElementById('id_cdp_issue_date');
        const cdp_numInput = document.getElementById('id_cdp_number');
        const holderInput = document.getElementById('id_holder_position');
        const chargeInput = document.getElementById('id_incharge_position');

        cdp_dateInput.setAttribute('readonly', true)
        cdp_numInput.setAttribute('readonly', true)
        holderInput.setAttribute('readonly', true)
        chargeInput.setAttribute('readonly', true)

        if (withdrawalModeSelect.value === 'C') {
            const sell_sellerInput = document.getElementById('id_sell_seller');
            const sell_typeInput = document.getElementById('id_sell_doc_type');
            const sell_numInput = document.getElementById('id_sell_doc_num');

            sell_sellerInput.setAttribute('readonly', true)
            sell_typeInput.setAttribute('readonly', true)
            sell_numInput.setAttribute('readonly', true)
        }

        if (withdrawalModeSelect.value === 'D') {
            const def_resoInput = document.getElementById('id_def_resolution');
            const def_dateInput = document.getElementById('id_def_date');
            const def_posiInput = document.getElementById('id_def_position');

            def_resoInput.setAttribute('readonly', true)
            def_dateInput.setAttribute('readonly', true)
            def_posiInput.setAttribute('readonly', true)
        }
        
        if (withdrawalModeSelect.value === 'E') {
            const est_nitInput = document.getElementById('id_est_nit');
            const est_instInput = document.getElementById('id_est_institution');
           
            est_nitInput.setAttribute('readonly', true)
            est_instInput.setAttribute('readonly', true)
        }

        if (withdrawalModeSelect.value === 'H') {
            const hip_loanInput = document.getElementById('id_hip_loan_number');
            const hip_nitInput = document.getElementById('id_hip_nit');
            const hip_bankInput = document.getElementById('id_hip_bank');
            
            hip_loanInput.setAttribute('readonly', true)
            hip_nitInput.setAttribute('readonly', true)
            hip_bankInput.setAttribute('readonly', true)
        }
    }
    // Estados NOTIFICADO BLOQUEA LA MODIFICACION DE LA INFORMACION DE LA SOLICITUD EN GENERAL ANTES PERMITIA MODIFICAR LOS VALORES DEL CALCULO
    if (!requestStateValue || !['1','2','3','4','5','6'].includes(requestStateValue)) {
        // Obtener los elementos del formulario
        const noti_dateInput = document.getElementById('id_notify_date');

        const nowork_daysInput = document.getElementById('id_no_work_days');

        const wageInput = document.getElementById('id_wage');
        const overwageInput = document.getElementById('id_overwage');
        const annual_bonusInput = document.getElementById('id_annual_bonus');
        const holiday_bonusInput = document.getElementById('id_holiday_bonus');
        const christmas_bonusInput = document.getElementById('id_christmas_bonus');
        const bonusInput = document.getElementById('id_bonus');
        const transport_subsidyInput = document.getElementById('id_transport_subsidy');
        const food_subsidynput = document.getElementById('id_food_subsidy');
        const technical_bonusInput = document.getElementById('id_technical_bonus');
        const seniority_bonusInput = document.getElementById('id_seniority_bonus');
        const accommodation_bonusInput = document.getElementById('id_accommodation_bonus');
        const overtimeInput = document.getElementById('id_overtime');
        const dev_by_drawInput = document.getElementById('id_dev_by_draw');
        const travel_expensesnput = document.getElementById('id_travel_expenses');
 
        const reso_dateInput = document.getElementById('id_resolution_date');
        const reso_numInput = document.getElementById('id_resolution_number');

        reso_dateInput.setAttribute('readonly', true)
        reso_numInput.setAttribute('readonly', true)

        noti_dateInput.setAttribute('readonly', true)

        nowork_daysInput.setAttribute('readonly', true)

        wageInput.setAttribute('readonly', true)
        overwageInput.setAttribute('readonly', true)
        annual_bonusInput.setAttribute('readonly', true)
        holiday_bonusInput.setAttribute('readonly', true)
        christmas_bonusInput.setAttribute('readonly', true)
        bonusInput.setAttribute('readonly', true)
        transport_subsidyInput.setAttribute('readonly', true)
        food_subsidynput.setAttribute('readonly', true)
        technical_bonusInput.setAttribute('readonly', true)
        seniority_bonusInput.setAttribute('readonly', true)
        accommodation_bonusInput.setAttribute('readonly', true)
        overtimeInput.setAttribute('readonly', true)
        dev_by_drawInput.setAttribute('readonly', true)
        travel_expensesnput.setAttribute('readonly', true)
    }

    if (!requestStateValue || !['1','2','3','4','5','6','7','8','9'].includes(requestStateValue)) {
        // Obtener los elementos del formulario
        const rpc_dateInput = document.getElementById('id_rpc_request_date');
        const rpc_numInput = document.getElementById('id_rpc_number');

        rpc_dateInput.setAttribute('readonly', true)
        rpc_numInput.setAttribute('readonly', true)
    }

    if (['11'].includes(requestStateValue)) {
        // Obtener los elementos del formulario
        const treasury_dateInput = document.getElementById('id_treasury_date');
        const billing_dateInput = document.getElementById('id_billing_date');
        const billing_numInput = document.getElementById('id_billing_number');

        treasury_dateInput.setAttribute('readonly', true)
        billing_dateInput.setAttribute('readonly', true)
        billing_numInput.setAttribute('readonly', true)
    }
});