// ADMIN_PERFIL.JS - Funcionalidades do perfil do admin

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.perfil-form');
    const passwordInput = document.getElementById('password');
    const passwordConfirmInput = document.getElementById('password_confirm');

    // Validação de senha
    if (form) {
        form.addEventListener('submit', function(e) {
            if (passwordInput.value !== passwordConfirmInput.value) {
                e.preventDefault();
                alert('As senhas não coincidem!');
                return false;
            }

            if (passwordInput.value && passwordInput.value.length < 8) {
                e.preventDefault();
                alert('A senha deve ter pelo menos 8 caracteres!');
                return false;
            }
        });
    }

    // Botão de alterar avatar
    const btnChangeAvatar = document.querySelector('.btn-change-avatar');
    if (btnChangeAvatar) {
        btnChangeAvatar.addEventListener('click', function() {
            alert('Funcionalidade de upload de imagem em desenvolvimento');
        });
    }

    // Animação de entrada
    const perfilCard = document.querySelector('.perfil-card');
    if (perfilCard) {
        perfilCard.style.animation = 'fadeInUp 0.5s ease-out';
    }

    const perfilSidebar = document.querySelector('.perfil-sidebar');
    if (perfilSidebar) {
        perfilSidebar.style.animation = 'fadeInUp 0.5s ease-out 0.1s both';
    }
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