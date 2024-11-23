document.addEventListener('DOMContentLoaded', function () {
    
    // Función que calcula el valor y lo asigna al campo destino
    function calculateValues(factor, originFieldId, targetFieldId) {
        const originField = document.getElementById(originFieldId);
        const targetField = document.getElementById(targetFieldId);

        const originValue = parseFloat(originField.value) || 0;
        const calculatedValue = originValue / factor;

        targetField.value = calculatedValue >= 0 ? calculatedValue.toFixed(0) : 0;

        calculateAVGwage();
    }

    function calculateAVGwage() {
        const fields = [
            'wage_doc', 'overwage_doc', 'annual_bonus_doc', 'holiday_bonus_doc', 
            'christmas_bonus_doc', 'bonus_doc', 'transport_subsidy_doc', 'food_subsidy_doc', 
            'technical_bonus_doc', 'seniority_bonus_doc', 'accommodation_bonus_doc', 
            'overtime_doc', 'dev_by_draw_doc', 'travel_expenses_doc'
        ];
        
        const avgsalaryField = document.getElementById('id_average_salary');
        const totalWage = fields.reduce((sum, fieldId) => sum + (parseFloat(document.getElementById(fieldId).value) || 0), 0);
        avgsalaryField.value = totalWage >= 0 ? totalWage.toFixed(2) : 0;
        
        calculateTotalseverance();
    }

    function calculateTotalseverance() {
        const totalSeveranceField = document.getElementById('id_total_severance_value');
        const balanceSeveranceField = document.getElementById('id_balance_severance');
        const AVGwage = parseFloat(document.getElementById('id_average_salary').value) || 0;
        const workDays = parseFloat(document.getElementById('id_working_days').value) || 0;
        const PrevSever = parseFloat(document.getElementById('id_previous_severance_value').value) || 0;

        const TotalSever = (AVGwage * workDays) / 360;
        const BalanceSever = TotalSever - PrevSever;

        totalSeveranceField.value = TotalSever >= 0 ? TotalSever.toFixed(2) : 0;
        balanceSeveranceField.value = BalanceSever >= 0 ? BalanceSever.toFixed(2) : 0;

        calculateDisbursedseverance();
    }

    function calculateDisbursedseverance() {
        const withdrawField = document.getElementById('id_withdrawal_mode');
        const fillingField = document.getElementById('id_filling_value');
        const balanceSeveranceField = document.getElementById('id_balance_severance');
        const disbursedSeveranceField = document.getElementById('id_severance_disbursed_value');

        const filling = parseFloat(fillingField.value) || 0;
        const balance = parseFloat(balanceSeveranceField.value) || 0;
        let disbursed = 0;

        if (withdrawField.value === "D") {
            disbursed = balance;
        } else {
            disbursed = filling > balance ? balance : filling;
        }

        disbursedSeveranceField.value = disbursed >= 0 ? disbursed.toFixed(2) : 0;
    }

    function formatCurrency(input) {
        let value = parseFloat(input.value.replace(/[^0-9.-]+/g, ""));
        if (!isNaN(value)) {
            input.value = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
            }).format(value);
        }
    }
    // Mapear los campos con sus factores y objetivos
    const fieldMapping = [
        { origin: 'id_wage', target: 'wage_doc', factor: 1 },
        { origin: 'id_overwage', target: 'overwage_doc', factor: 1 },
        { origin: 'id_annual_bonus', target: 'annual_bonus_doc', factor: 12 },
        { origin: 'id_holiday_bonus', target: 'holiday_bonus_doc', factor: 12 },
        { origin: 'id_christmas_bonus', target: 'christmas_bonus_doc', factor: 12 },
        { origin: 'id_bonus', target: 'bonus_doc', factor: 12 },
        { origin: 'id_transport_subsidy', target: 'transport_subsidy_doc', factor: 1 },
        { origin: 'id_food_subsidy', target: 'food_subsidy_doc', factor: 1 },
        { origin: 'id_technical_bonus', target: 'technical_bonus_doc', factor: 1 },
        { origin: 'id_seniority_bonus', target: 'seniority_bonus_doc', factor: 1 },
        { origin: 'id_accommodation_bonus', target: 'accommodation_bonus_doc', factor: 12 },
        { origin: 'id_overtime', target: 'overtime_doc', factor: 12 },
        { origin: 'id_dev_by_draw', target: 'dev_by_draw_doc', factor: 12 },
        { origin: 'id_travel_expenses', target: 'travel_expenses_doc', factor: 12 }
    ];

    // Añadir eventos de manera dinámica
    fieldMapping.forEach(({ origin, target, factor }) => {
        document.getElementById(origin).addEventListener('input', function () {
            calculateValues(factor, origin, target);
        });

        // Calcular y mostrar valores al cargar la página
        calculateValues(factor, origin, target);
    });

    const requestDateField = document.getElementById('id_cutoff_date');
    requestDateField.addEventListener('blur', function() {
        calculateTotalseverance();
    });

    const noWorkField = document.getElementById('id_no_work_days');
    noWorkField.addEventListener('blur', function() {
        calculateTotalseverance();
    });

    // Añadir el event listener al campo id_filling_value para calcular disbursed severance
    const fillingField = document.getElementById('id_filling_value');
    fillingField.addEventListener('blur', function() {
        calculateDisbursedseverance();
    });

    // Añadir el event listener al campo id_filling_value para calcular disbursed severance
    const withdrawField = document.getElementById('id_withdrawal_mode');
    withdrawField.addEventListener('blur', function() {
        calculateDisbursedseverance();
    });


});
