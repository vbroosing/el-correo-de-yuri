document.addEventListener('DOMContentLoaded', function() {
    console.log("Script de filtros cargado correctamente.");

    // 1. Obtener referencias a los selects
    const selectArea = document.getElementById('select-area');
    const selectDepto = document.getElementById('select-departamento');
    const selectCargo = document.getElementById('select-cargo');

    if (!selectArea || !selectDepto || !selectCargo) {
        console.error("Error: No se encontraron los selectores con los IDs esperados.");
        return;
    }

    // 2. Guardar TODAS las opciones originales en memoria (clonando los datos)
    // Esto previene que se pierdan al limpiar el HTML
    const dataDepartamentos = Array.from(selectDepto.querySelectorAll('option')).map(opt => ({
        value: opt.value,
        text: opt.textContent,
        areaId: opt.getAttribute('data-area-id')
    }));

    const dataCargos = Array.from(selectCargo.querySelectorAll('option')).map(opt => ({
        value: opt.value,
        text: opt.textContent,
        deptoId: opt.getAttribute('data-departamento-id'),
        areaId: opt.getAttribute('data-area-id')
    }));

    // Función auxiliar para reconstruir un select
    function llenarSelect(selectElement, opciones, filtroFn) {
        // Guardar valor actual por si podemos mantenerlo
        const valorActual = selectElement.value;
        
        // Limpiar
        selectElement.innerHTML = '';

        // Filtrar y agregar
        opciones.forEach(dato => {
            // Siempre agregar la opción vacía (placeholder) o si pasa el filtro
            if (dato.value === "" || filtroFn(dato)) {
                const option = document.createElement('option');
                option.value = dato.value;
                option.textContent = dato.text;
                // Restaurar atributos de datos por si se necesitan luego
                if (dato.areaId) option.setAttribute('data-area-id', dato.areaId);
                if (dato.deptoId) option.setAttribute('data-departamento-id', dato.deptoId);
                
                selectElement.appendChild(option);
            }
        });

        // Intentar restaurar selección si aún es válida, si no, resetear
        // (Verificamos si el valorActual existe en las nuevas opciones del select)
        const existe = Array.from(selectElement.options).some(opt => opt.value === valorActual);
        if (existe && valorActual !== "") {
            selectElement.value = valorActual;
        } else {
            selectElement.value = "";
        }
    }

    // --- EVENTOS ---

    // 1. Cambio en ÁREA
    selectArea.addEventListener('change', function() {
        const areaId = this.value;
        console.log("Área cambiada a:", areaId);

        // Filtrar Departamentos: Mostrar solo los de esta área
        llenarSelect(selectDepto, dataDepartamentos, (d) => d.areaId === areaId);

        // Filtrar Cargos: Mostrar solo los de esta área (opcional, pero mejora UX)
        llenarSelect(selectCargo, dataCargos, (c) => c.areaId === areaId);
    });

    // 2. Cambio en DEPARTAMENTO
    selectDepto.addEventListener('change', function() {
        const deptoId = this.value;
        console.log("Departamento cambiado a:", deptoId);

        if (deptoId) {
            // a) Autocompletar Área hacia arriba
            const deptoInfo = dataDepartamentos.find(d => d.value === deptoId);
            if (deptoInfo && deptoInfo.areaId) {
                if (selectArea.value !== deptoInfo.areaId) {
                    selectArea.value = deptoInfo.areaId;
                    // IMPORTANTE: Al cambiar el área programáticamente, debemos refrescar sus dependencias visuales
                    // pero sin borrar la selección actual de departamento.
                    // Sin embargo, como el depto ya es válido para el área, solo filtramos cargos.
                }
            }

            // b) Filtrar Cargos hacia abajo (solo de este depto)
            llenarSelect(selectCargo, dataCargos, (c) => c.deptoId === deptoId);
        } else {
            // Si selecciona "Seleccionar departamento" (vacío), restaurar cargos según el Área actual
            const areaId = selectArea.value;
            if (areaId) {
                 llenarSelect(selectCargo, dataCargos, (c) => c.areaId === areaId);
            } else {
                 llenarSelect(selectCargo, dataCargos, () => true); // Mostrar todos si no hay nada
            }
        }
    });

    // 3. Cambio en CARGO
    selectCargo.addEventListener('change', function() {
        const cargoId = this.value;
        console.log("Cargo cambiado a:", cargoId);

        if (cargoId) {
            const cargoInfo = dataCargos.find(c => c.value === cargoId);
            
            if (cargoInfo) {
                // a) Autocompletar Área (Nivel superior)
                if (cargoInfo.areaId && selectArea.value !== cargoInfo.areaId) {
                    selectArea.value = cargoInfo.areaId;
                    // Al cambiar área, deberíamos filtrar deptos para que el usuario solo vea los de esa área
                    llenarSelect(selectDepto, dataDepartamentos, (d) => d.areaId === cargoInfo.areaId);
                }

                // b) Autocompletar Departamento (Nivel medio)
                if (cargoInfo.deptoId && selectDepto.value !== cargoInfo.deptoId) {
                    // Asegurarnos que el depto esté disponible en la lista (ya lo hicimos arriba al filtrar por área)
                    selectDepto.value = cargoInfo.deptoId;
                }
            }
        }
    });
});