
// Función de autocompletar
function autocomplete(inputSelector, resultsSelector, service, fieldMapping, clearFieldsFunction) {
    var selectedItem = null;
    $(document).on('input', inputSelector, function() {
        var query = $(this).val();
        var url = $(this).data('url');
        var finalUrl = `${url}?q=${query}&service=${service}`;      
        if (query.length > 2) { 
            $.ajax({
                url: finalUrl,
                data: {
                    'q': query
                },
                dataType: 'json',
                success: function(data) {
                    $(resultsSelector).empty();
                    
                        $.each(data.results, function(index, item) {
                            var listItem = $('<li>').addClass('autocomplete-item');
                        
                            // Agregar atributos dinámicamente según el fieldMapping
                            $.each(fieldMapping, function(dataField, _) {
                                // Verificar si el item tiene el campo en su estructura
                                    listItem.attr('data-' + dataField, item[dataField]);
                            });
                            // Asignar el texto del elemento
                            listItem.text(item.text);
                            // Agregar el elemento a la lista de resultados
                            $(resultsSelector).append(listItem);
                        });

                    $('.autocomplete-item').on('click', function() {
                        selectedItem = $(this);
                        fillFields($(this), fieldMapping);  // Llenar los campos
                        $(resultsSelector).empty();  // Limpiar la lista de autocompletado
                    });
                },
                error: function(xhr, status, error) {
                    console.error("Error en la solicitud AJAX:", error);
                }
            });            
        } else {
            $(resultsSelector).empty();  // Limpiar la lista de autocompletado
            $results.hide(); // Oculta la lista si no hay resultados
        }
    });

    // Limpiar campos si el valor en el input cambia
    $(document).on('input', inputSelector, function() {  
        const keyName = Object.keys(fieldMapping).find(key => fieldMapping[key] === inputSelector);
        if (selectedItem && $(this).val() !== selectedItem.data(keyName)) {
            clearFieldsFunction();
        }
    });
}

function clearfieldOnload(inputSelector) {
    $(document).ready(function() {
        var initialValue = $(inputSelector).val(); // Capturar el valor al cargar la pantalla
        var previousValue = initialValue; // Asignar este valor como el valor previo
        if (initialValue) {
            $(inputSelector).val(initialValue); // Asignar el valor al campo de autocompletar
        }

        // Comparar el valor actual con el valor capturado cuando el input cambia
        $(document).on('input', inputSelector, function() {
            var currentValue = $(this).val(); // Obtener el valor actual del input
            // Si el valor ha cambiado, limpiar los campos relacionados
            if (currentValue !== previousValue) {
                clearFields();
            }
        });
    });
}

// Función para limpiar los campos si se mapean más de un campo
function clearFields() {
    // Solo limpiamos si hay más de un campo en el mapeo
    $('.clearable-field').each(function() {
        const block = $(this).data('block');
        if (block === 1) {
            $(this).val('').prop('readonly', true); // Deshabilita y limpia
        } else if (block === 2) {
            $(this).val('').prop('readonly', false); // Habilita y limpia
        }
    });
}

// Función para llenar los campos del formulario, basada en el mapeo
function fillFields(selectedItem, fieldMapping) {    
    $.each(fieldMapping, function(dataField, selector) {        
        $(selector).val(selectedItem.data(dataField));
        // Condicional para ejecutar fetchPreviousSeveranceValue si se llena 'numid'
        if (dataField === 'severancePrev') {
            var numberID = selectedItem.data('vnumber_id');
            fetchPreviousSeveranceValue(numberID);
        }
    });
}

function fetchPreviousSeveranceValue(number_ID) {
    fetch(`../get_previous_severance_value_ajax/${number_ID}/`)
        .then(response => response.json())
        .then(data => {
            $('#id_previous_severance_value').val(data.previous_severance_value || 0);
            // Llamar a la función para renderizar la historia en el template
            renderHistory(data.history);
        })
        .catch(error => console.error('Error fetching severance value:', error));
}

function renderHistory(history) {
    const historyTableBody = $('#history-table tbody'); // Asumiendo que tienes una tabla con ID 'history-table'
    historyTableBody.empty(); // Limpiar tabla existente

    // Llenar la tabla con datos de history
    history.forEach(hist => {
        historyTableBody.append(`
            <tr>
                <td>${hist.request_ID}</td>
                <td>${hist.resolution_number}</td>
                <td>${hist.resolution_date}</td>
                <td>${hist.severance_disbursed_value}</td>
            </tr>
        `);
    });
}

// JavaScript con jQuery para manejar el Datepicker
$(document).ready(function() {
    // Función para inicializar el datepicker
    function initializeDatepicker() {
        $('.datepicker').each(function() {
            if (!$(this).prop('readonly')) {  // Solo inicializa si el elemento no tiene readonly
                $(this).datepicker({
                    format: 'dd/mm/yyyy',
                    autoclose: true,
                    todayHighlight: true,
                    placeholder: 'Ingrese fecha',
                }).on('changeDate', function() {
                    calculateDays(); // Llama directamente a calculateDays si el datepicker está activo
                });
            } else {
                // Si el campo es readonly, destruye el datepicker si ya está inicializado
                $(this).datepicker('destroy');
            }
        });
    }

    // Inicializa el datepicker al cargar la página
    initializeDatepicker();

    // Escucha cambios en todos los campos de tipo datepicker para re-inicializar si es necesario
    $('.datepicker').on('change', function() {
        initializeDatepicker(); // Re-inicializa el datepicker para reflejar el estado actual
    });
});
