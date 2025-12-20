document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Referencias
    const selectArea = document.getElementById('select-area');
    const selectDepto = document.getElementById('select-departamento');
    const selectCargo = document.getElementById('select-cargo');

    // 2. Copia maestra de los datos (para poder restaurarlos al filtrar)
    const dataDeptos = Array.from(selectDepto.options).map(o => ({
        val: o.value, text: o.text, area: o.dataset.areaId 
    }));
    const dataCargos = Array.from(selectCargo.options).map(o => ({
        val: o.value, text: o.text, depto: o.dataset.departamentoId, area: o.dataset.areaId 
    }));

    // Función auxiliar para repoblar selects
    function actualizarSelect(select, datos, filtro) {
        select.innerHTML = ''; // Limpiar
        datos.forEach(d => {
            // Mostrar si es placeholder (val="") O cumple el filtro
            if (d.val === "" || filtro(d)) {
                const opt = document.createElement('option');
                opt.value = d.val;
                opt.text = d.text;
                // Restaurar atributos por si se necesitan luego
                if (d.area) opt.dataset.areaId = d.area;
                if (d.depto) opt.dataset.departamentoId = d.depto;
                select.appendChild(opt);
            }
        });
    }

    // --- EVENTOS ---

    // A. CAMBIO ÁREA -> Filtra Deptos y Cargos
    selectArea.addEventListener('change', function() {
        const areaId = this.value;
        selectDepto.value = ""; 
        selectCargo.value = "";

        // Si hay área seleccionada, filtra. Si no, muestra todo.
        if (areaId) {
            actualizarSelect(selectDepto, dataDeptos, d => d.area === areaId);
            actualizarSelect(selectCargo, dataCargos, c => c.area === areaId);
        } else {
            actualizarSelect(selectDepto, dataDeptos, () => true);
            actualizarSelect(selectCargo, dataCargos, () => true);
        }
    });

    // B. CAMBIO DEPTO -> Filtra Cargos y Autoselecciona Área
    selectDepto.addEventListener('change', function() {
        const deptoId = this.value;
        const opcion = this.options[this.selectedIndex];
        
        if (deptoId) {
            // Autoseleccionar área padre
            const areaId = opcion.dataset.areaId;
            if (areaId && selectArea.value !== areaId) {
                selectArea.value = areaId; 
                // Al cambiar el área visualmente, podríamos querer re-filtrar el depto, 
                // pero ya estamos en el depto correcto.
            }
            // Filtrar cargos hijos
            selectCargo.value = "";
            actualizarSelect(selectCargo, dataCargos, c => c.depto === deptoId);
        } else {
            // Si resetea depto, restaurar cargos según el área que quede
            const areaId = selectArea.value;
            if(areaId) {
                actualizarSelect(selectCargo, dataCargos, c => c.area === areaId);
            } else {
                actualizarSelect(selectCargo, dataCargos, () => true);
            }
        }
    });

    // C. CAMBIO CARGO -> Autoselecciona Depto y Área
    selectCargo.addEventListener('change', function() {
        const cargoId = this.value;
        const opcion = this.options[this.selectedIndex];

        if (cargoId) {
            const deptoId = opcion.dataset.departamentoId;
            const areaId = opcion.dataset.areaId;

            // Poner el Área
            if (areaId && selectArea.value !== areaId) {
                selectArea.value = areaId;
                // Al cambiar área, los deptos deberían filtrarse para ser consistentes
                actualizarSelect(selectDepto, dataDeptos, d => d.area === areaId);
            }

            // Poner el Depto
            if (deptoId) {
                selectDepto.value = deptoId;
            }
        }
    });
});