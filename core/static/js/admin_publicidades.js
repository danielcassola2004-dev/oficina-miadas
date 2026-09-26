// ADMIN_PUBLICIDADES.JS - Funcionalidades da gestão de publicidades

document.addEventListener('DOMContentLoaded', function() {
    // Animações ao carregar
    const publicidadeCards = document.querySelectorAll('.publicidade-card');
    publicidadeCards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.5s ease-out ${index * 0.1}s both`;
    });

    // Confirmar exclusão
    const deleteLinks = document.querySelectorAll('a[href*="remover"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja remover esta publicidade?')) {
                e.preventDefault();
            }
        });
    });
});

// Animação de fade in up
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);