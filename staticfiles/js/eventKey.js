
    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        // Permite números y teclas de control
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        return true;
    }

    function isCharKey(evt) {
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        // Permitir letras (mayúsculas y minúsculas) y espacios
        if (charCode < 65 || (charCode > 90 && charCode < 97) || charCode > 122) {
            // Si no es una letra y no es un espacio (charCode 32), evitar la entrada
            if (charCode !== 32) {
                return false;
            }
        }
        return true;
    }

    function formatCurrency(input) {
        // Remover cualquier carácter no numérico excepto el punto
        let value = input.value.replace(/[^0-9.-]+/g, "");
        
        // Convertir a número
        let numValue = parseFloat(value);
        
        if (!isNaN(numValue)) {
            // Formatear con separador de miles
            input.value = numValue.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }
    }
    
    function clearFormatting(input) {
        // Remover el formato al enfocar
        let value = input.value.replace(/[^0-9.-]+/g, "");
        input.value = value;
    }

