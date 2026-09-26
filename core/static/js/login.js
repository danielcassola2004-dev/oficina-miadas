/* ============================================================
   ARQUIVO: login_seguro.js
   DESCRIÇÃO: Validação e segurança para formulário de login
   IDIOMA: Português
   ============================================================ */

// ============================================================
// SEÇÃO 1: INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Script de login seguro carregado');
    
    // Comentário: Inicializar validações
    inicializarValidacoes();
    inicializarTogglePassword();
});

// ============================================================
// SEÇÃO 2: VALIDAÇÕES
// ============================================================

function inicializarValidacoes() {
    // Comentário: Obter formulário
    const form = document.getElementById('formLogin');
    const inputs = form.querySelectorAll('input[type="text"], input[type="password"]');
    
    // Comentário: Adicionar validação em tempo real
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validarCampo(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('invalid')) {
                validarCampo(this);
            }
        });
    });
    
    // Comentário: Validar ao submeter
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validarFormulario()) {
            this.submit();
        }
    });
}

// ============================================================
// SEÇÃO 3: VALIDAR CAMPO INDIVIDUAL
// ============================================================

function validarCampo(input) {
    // Comentário: Obter grupo do campo
    const formGroup = input.closest('.form-group');
    const feedback = formGroup.querySelector('.validation-feedback');
    let valido = true;
    let mensagem = '';
    
    // Comentário: Validações específicas por tipo
    if (input.name === 'username') {
        // Comentário: Validar nome de utilizador
        if (input.value.length < 3) {
            valido = false;
            mensagem = 'Nome de utilizador deve ter pelo menos 3 caracteres';
        }
    } else if (input.name === 'password') {
        // Comentário: Validar senha
        if (input.value.length === 0) {
            valido = false;
            mensagem = 'Palavra-passe é obrigatória';
        }
    }
    
    // Comentário: Aplicar resultado da validação
    if (valido) {
        input.classList.remove('invalid');
        input.classList.add('valid');
        if (feedback) feedback.textContent = '';
    } else {
        input.classList.remove('valid');
        input.classList.add('invalid');
        if (feedback) feedback.textContent = mensagem;
    }
    
    return valido;
}

// ============================================================
// SEÇÃO 4: VALIDAR FORMULÁRIO COMPLETO
// ============================================================

function validarFormulario() {
    // Comentário: Obter todos os inputs
    const form = document.getElementById('formLogin');
    const inputs = form.querySelectorAll('input[type="text"], input[type="password"]');
    
    let formularioValido = true;
    
    // Comentário: Validar cada campo
    inputs.forEach(input => {
        if (!validarCampo(input)) {
            formularioValido = false;
        }
    });
    
    if (!formularioValido) {
        console.log('❌ Formulário inválido');
        mostrarNotificacao('Por favor, preencha todos os campos corretamente', 'error');
    }
    
    return formularioValido;
}

// ============================================================
// SEÇÃO 5: TOGGLE DE VISIBILIDADE DE SENHA
// ============================================================

function inicializarTogglePassword() {
    // Comentário: Adicionar evento aos botões de toggle
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.closest('.password-wrapper').querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
}

function togglePassword(inputId) {
    // Comentário: Função auxiliar para toggle de senha
    const input = document.getElementById(inputId);
    const button = input.closest('.password-wrapper').querySelector('.toggle-password');
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// ============================================================
// SEÇÃO 6: NOTIFICAÇÕES
// ============================================================

function mostrarNotificacao(mensagem, tipo = 'sucesso') {
    // Comentário: Mostrar notificação
    const notificacao = document.createElement('div');
    notificacao.className = `notificacao notificacao-${tipo}`;
    notificacao.textContent = mensagem;
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        background: ${tipo === 'sucesso' ? '#28a745' : '#dc3545'};
        color: white;
        font-weight: 600;
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notificacao);
    
    setTimeout(() => {
        notificacao.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notificacao.remove(), 300);
    }, 3000);
}

// ============================================================
// SEÇÃO 7: PROTEÇÃO CONTRA FORÇA BRUTA
// ============================================================

function protegerContraForcaBruta() {
    // Comentário: Limitar tentativas de login
    const tentativasKey = 'loginTentativas';
    const tempoKey = 'loginTempo';
    
    let tentativas = localStorage.getItem(tentativasKey) || 0;
    let tempo = localStorage.getItem(tempoKey);
    
    // Comentário: Verificar se passou 15 minutos
    if (tempo && Date.now() - parseInt(tempo) > 15 * 60 * 1000) {
        tentativas = 0;
        localStorage.removeItem(tempoKey);
    }
    
    // Comentário: Se mais de 5 tentativas, bloquear
    if (tentativas >= 5) {
        mostrarNotificacao('Muitas tentativas de login. Tente novamente em 15 minutos.', 'error');
        document.getElementById('formLogin').style.display = 'none';
        return false;
    }
    
    return true;
}

// ============================================================
// SEÇÃO 8: ESTILOS DINÂMICOS
// ============================================================

// Comentário: Adicionar estilos dinâmicos
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('✅ Todos os scripts de login seguro inicializados com sucesso!');
