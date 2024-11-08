
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
        }
    });

    // Limpiar campos si el valor en el input cambia
    $(document).on('input', inputSelector, function() {        
        if (selectedItem && $(this).val() !== selectedItem.data('vnumber_id')) {
            clearFieldsFunction(fieldMapping,inputSelector);
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

// Función para limpiar los campos si se mapean más de un campo
function clearFields(fieldMapping,inputSelector) {
    // Solo limpiamos si hay más de un campo en el mapeo
    if (Object.keys(fieldMapping).length > 1) {
        $.each(fieldMapping, function(_, selector) {
            // Comprobar si el selector no es el campo actual
            if (selector !== inputSelector) {
                $(selector).val('').prop('disabled', true);
            }
        });
    }
}

// Función para obtener el valor de cesantías anteriores (llamada condicionalmente)
function fetchPreviousSeveranceValue(number_ID) {
    fetch(`../get_previous_severance_value_ajax/${number_ID}/`)
        .then(response => response.json())
        .then(data => {
            $('#id_previous_severance_value').val(data.previous_severance_value || 0);
        })
        .catch(error => console.error('Error fetching severance value:', error));
}
