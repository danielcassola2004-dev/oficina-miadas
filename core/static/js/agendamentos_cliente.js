// Filtros já funcionam com form submit
// Este ficheiro pode ser expandido com funcionalidades AJAX

document.addEventListener('DOMContentLoaded', function() {
    // Animações de entrada
    const items = document.querySelectorAll('.appointment-item');
    items.forEach((item, index) => {
        item.style.animation = `slideUp 0.5s ease ${index * 0.1}s both`;
    });
});