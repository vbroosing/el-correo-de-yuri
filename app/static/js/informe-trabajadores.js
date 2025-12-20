document.addEventListener('DOMContentLoaded', function() {
    const selectArea = document.getElementById('select-area');
    const selectDepto = document.getElementById('select-departamento');
    const selectCargo = document.getElementById('select-cargo');

    // Guardamos las opciones originales para poder restaurarlas al filtrar
    const opcionesDeptoOriginales = Array.from(selectDepto.options);
    const opcionesCargoOriginales = Array.from(selectCargo.options);

    // 1. LOGICA AL CAMBIAR ÁREA
    selectArea.addEventListener('change', function() {
        const areaId = this.value;

        // Filtrar Departamentos
        selectDepto.innerHTML = ''; // Limpiar
        opcionesDeptoOriginales.forEach(opcion => {
            // Mostrar si es el placeholder (value="") o coincide el área
            if (opcion.value === "" || opcion.dataset.areaId === areaId || areaId === "") {
                selectDepto.appendChild(opcion);
            }
        });
        selectDepto.value = ""; // Resetear selección

        // Filtrar Cargos (Mostrar todos los cargos de esa área)
        selectCargo.innerHTML = ''; // Limpiar
        opcionesCargoOriginales.forEach(opcion => {
            if (opcion.value === "" || opcion.dataset.areaId === areaId || areaId === "") {
                selectCargo.appendChild(opcion);
            }
        });
        selectCargo.value = ""; // Resetear selección
    });

    // 2. LOGICA AL CAMBIAR DEPARTAMENTO
    selectDepto.addEventListener('change', function() {
        const deptoId = this.value;
        const opcionSeleccionada = this.options[this.selectedIndex];
        
        // Autocompletar Área (hacia arriba)
        if (deptoId && opcionSeleccionada.dataset.areaId) {
            selectArea.value = opcionSeleccionada.dataset.areaId;
        }

        // Filtrar Cargos (hacia abajo)
        selectCargo.innerHTML = '';
        opcionesCargoOriginales.forEach(opcion => {
            // Mostrar si es placeholder o coincide el departamento
            if (opcion.value === "" || opcion.dataset.departamentoId === deptoId || deptoId === "") {
                selectCargo.appendChild(opcion);
            }
        });
        // Si el usuario deselecciona departamento (vuelve a ""), restauramos cargos según el área actual
        if (deptoId === "") {
            const areaActual = selectArea.value;
            // Disparamos el evento de área manualmente para re-filtrar
            selectArea.dispatchEvent(new Event('change')); 
        } else {
            selectCargo.value = "";
        }
    });

    // 3. LOGICA AL CAMBIAR CARGO
    selectCargo.addEventListener('change', function() {
        const cargoId = this.value;
        const opcionSeleccionada = this.options[this.selectedIndex];

        if (cargoId) {
            // Autocompletar Departamento
            const deptoId = opcionSeleccionada.dataset.departamentoId;
            if (deptoId) {
                selectDepto.value = deptoId;
                
                // Al setear el valor manualmente, debemos asegurar que las opciones sean visibles
                // (por si estaban ocultas por un filtro previo incorrecto)
                // Una forma rápida es disparar el evento del departamento para que chequee el área
                    selectDepto.dispatchEvent(new Event('change'));
                    
                    // Volvemos a poner el cargo (porque el evento change de depto lo borra al filtrar)
                    selectCargo.value = cargoId;
            }
        }
    });
});