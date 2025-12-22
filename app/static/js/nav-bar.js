document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Seleccionamos el botón del menú hamburguesa
    // Usamos la clase .navbar-toggler que ya tiene tu HTML
    const botonMenu = document.querySelector('.navbar-toggler');
    
    // 2. Seleccionamos el contenido del menú que se debe desplegar
    // Usamos el ID que tiene tu div: id="navbarSupportedContent"
    const menuDesplegable = document.getElementById('navbarSupportedContent');

    // 3. Verificamos que existan para evitar errores
    if (botonMenu && menuDesplegable) {
        
        botonMenu.addEventListener('click', function() {
            // 4. Alternamos la clase 'show'
            // Bootstrap usa esta clase para aplicar display: block al menú móvil
            menuDesplegable.classList.toggle('show');
        });
    }
});