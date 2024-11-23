document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const startDateInput = document.getElementById('id_start_date');
    const cutoffDateInput = document.getElementById('id_cutoff_date');
    const totalDaysInput = document.getElementById('id_total_days');
    const noWorkDaysInput = document.getElementById('id_no_work_days');
    const workingDaysInput = document.getElementById('id_working_days');
    const withdrawalModeSelect = document.getElementById('id_withdrawal_mode');
    const fillingInput = document.getElementById('id_filling_value');
        
    // Función para calcular los días entre dos fechas
    window.calculateDays = function() {
        // Asegura que el campo start_date tiene un valor
        if (!startDateInput.value || !cutoffDateInput.value) return;

        // Extraer y transformar las fechas en días
        const [sdday, sdmonth, sdyear] = startDateInput.value.split('/');
        const startDays = parseInt(sdday) + parseInt(sdmonth) * 30 + parseInt(sdyear) * 360;
    
        const [rdday, rdmonth, rdyear] = cutoffDateInput.value.split('/');
        const requestDays = parseInt(rdday) + parseInt(rdmonth) * 30 + parseInt(rdyear) * 360;
    
        // Calcular la diferencia en días
        const dayDifference = Math.max(0, requestDays - startDays);
    
        // Asignar el resultado al campo correspondiente
        totalDaysInput.value = dayDifference;

        calculateWorkingDays();
    }

    // Función para calcular los días trabajados (working days)
    function calculateWorkingDays() {
        const totalDays = parseInt(totalDaysInput.value) || 0;
        const noWorkDays = parseInt(noWorkDaysInput.value) || 0;

        const workingDays = Math.max(0, totalDays - noWorkDays);
        workingDaysInput.value = workingDays;
    }

    // Función para actualizar el campo radicado según el modo de retiro
    function updateFilling() {
        if (withdrawalModeSelect.value === 'D') {
            fillingInput.value = 0;
            fillingInput.readOnly = true;
        } else {
            fillingInput.value = "";
            fillingInput.readOnly = false;
        }
    }

    function FillingValue() {
        if (withdrawalModeSelect.value === 'D') {
            fillingInput.value = 0;
            fillingInput.readOnly = true;
        }
    }

    // Agregar eventos para calcular días y actualizar radicado
    function addEventListeners() {
        cutoffDateInput.addEventListener('input', calculateDays);
        totalDaysInput.addEventListener('blur', calculateWorkingDays);
        noWorkDaysInput.addEventListener('blur', calculateWorkingDays);
        withdrawalModeSelect.addEventListener('change', updateFilling);
    }

    // Llamar a la función al cargar la página en caso de que ya haya un valor seleccionado
    addEventListeners();
    FillingValue();
});
