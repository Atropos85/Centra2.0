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

        const ipartes = startDateInput.value.split("/");

        const idia = (31-ipartes[0]); 
        const imes = ((12-ipartes[1])*30);  
        const iaño = (1+parseInt(ipartes[2])); 

        // Extraer y transformar las fechas en días
        const fpartes = cutoffDateInput.value.split("/");
        let fecha = new Date(fpartes[2],fpartes[1]-1,fpartes[0]);
        fecha.setDate(fecha.getDate() + 1);
        const fec =  fecha.toISOString().split('T')[0]
        const [year, month, day] = fec.split('-').map(Number);
        
        let fdia;

        if (month == fpartes[1]) {
            fdia = (fpartes[0]); 
        }
        else {
            fdia = 30; 
        }

        const fmes = ((fpartes[1]-1)*30);  
        const faño = (parseInt(fpartes[2]));  

        const dia1 = (parseInt(idia) + parseInt(imes) + parseInt(fdia))

        const mes1 = (fmes)
        const año1 = (((faño -iaño) * 12) * 30)
        // Calcular la diferencia en días

        const dayDifference = dia1 +  mes1 + año1;

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
