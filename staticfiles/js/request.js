document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const startDateInput = document.getElementById('id_start_date');
    const requestDateInput = document.getElementById('id_request_date');
    const totalDaysInput = document.getElementById('id_total_days');
    const noWorkDaysInput = document.getElementById('id_no_work_days');
    const workingDaysInput = document.getElementById('id_working_days');
    const fillingValueInput = document.getElementById('id_filling_values');

    // Función para calcular los días entre dos fechas
    function calculateDays() {
        const startDate = new Date(startDateInput.value);
        const requestDate = new Date(requestDateInput.value);

        // Verificar que ambas fechas sean válidas
        if (isValidDate(startDate) && isValidDate(requestDate)) {
            const dayDifference = Math.max(0, Math.ceil((requestDate - startDate) / (1000 * 3600 * 24))); // Diferencia en días
            totalDaysInput.value = dayDifference; // Mostrar solo números positivos
        } else {
            totalDaysInput.value = ''; // Limpiar si hay alguna fecha no válida
        }

        calculateWorkingDays(); // Actualiza días trabajados
    }

    // Función para calcular los días trabajados (working days)
    function calculateWorkingDays() {
        const totalDays = parseInt(totalDaysInput.value) || 0; // Asegurarse de que sean números
        const noWorkDays = parseInt(noWorkDaysInput.value) || 0;

        const workingDays = Math.max(0, totalDays - noWorkDays); // Restar días no trabajados de días totales
        workingDaysInput.value = workingDays; // Mostrar solo números positivos
    }

    // Función para validar si la fecha es válida
    function isValidDate(date) {
        return !isNaN(date.getTime());
    }

    // Función para agregar eventos
    function addEventListeners() {
        requestDateInput.addEventListener('blur', calculateDays);
        totalDaysInput.addEventListener('blur', calculateWorkingDays);
        noWorkDaysInput.addEventListener('blur', calculateWorkingDays);
    }

    // Agregar eventos
    addEventListeners();
});
