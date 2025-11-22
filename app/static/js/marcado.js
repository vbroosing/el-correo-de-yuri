function updateClock() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        document.getElementById('clock').textContent = `${hours}:${minutes}`;
    }

    // Actualizar inmediatamente al cargar la página
    updateClock();

    // Actualizar cada minuto (o cada segundo si prefieres)
    setInterval(updateClock, 1000); // cada 1000 ms = 1 segundo