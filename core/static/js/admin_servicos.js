// ADMIN_SERVICOS.JS - Funcionalidades da gestão de serviços

document.addEventListener('DOMContentLoaded', function() {
    // Animações ao carregar
    const servicoCards = document.querySelectorAll('.servico-card');
    servicoCards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.5s ease-out ${index * 0.1}s both`;
    });

    // Confirmar exclusão
    const deleteLinks = document.querySelectorAll('a[href*="deletar"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja deletar este serviço?')) {
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