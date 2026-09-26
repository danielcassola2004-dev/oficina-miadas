/* ============================================================
   ARQUIVO: cadastro_seguro.js
   DESCRIÇÃO: Validação e segurança para formulário de cadastro
   IDIOMA: Português
   ============================================================ */

// ============================================================
// SEÇÃO 1: INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Script de cadastro seguro carregado');
    
    // Comentário: Inicializar validações
    inicializarValidacoes();
    inicializarIndicadorForca();
    inicializarTogglePassword();
});

// ============================================================
// SEÇÃO 2: VALIDAÇÕES
// ============================================================

function inicializarValidacoes() {
    // Comentário: Obter formulário
    const form = document.getElementById('formCadastro');
    const inputs = form.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="checkbox"]');
    
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
        } else if (input.value.length > 20) {
            valido = false;
            mensagem = 'Nome de utilizador não pode exceder 20 caracteres';
        } else if (!/^[a-zA-Z0-9_-]+$/.test(input.value)) {
            valido = false;
            mensagem = 'Nome de utilizador só pode conter letras, números, _ e -';
        }
    } else if (input.name === 'email') {
        // Comentário: Validar email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value)) {
            valido = false;
            mensagem = 'Email inválido. Digite um email válido';
        }
    } else if (input.name === 'password1') {
        // Comentário: Validar senha
        if (input.value.length < 8) {
            valido = false;
            mensagem = 'Palavra-passe deve ter pelo menos 8 caracteres';
        }
    } else if (input.name === 'password2') {
        // Comentário: Validar confirmação de senha
        const password1 = document.getElementById('id_password1').value;
        if (input.value !== password1) {
            valido = false;
            mensagem = 'As palavras-passe não coincidem';
        }
    } else if (input.name === 'terms') {
        // Comentário: Validar checkbox de termos
        if (!input.checked) {
            valido = false;
            mensagem = 'Deve concordar com os termos e condições';
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
    const form = document.getElementById('formCadastro');
    const inputs = form.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="checkbox"]');
    
    let formularioValido = true;
    
    // Comentário: Validar cada campo
    inputs.forEach(input => {
        if (!validarCampo(input)) {
            formularioValido = false;
        }
    });
    
    if (!formularioValido) {
        console.log('❌ Formulário inválido');
        mostrarNotificacao('Por favor, corrija os erros acima', 'error');
    }
    
    return formularioValido;
}

// ============================================================
// SEÇÃO 5: INDICADOR DE FORÇA DE SENHA
// ============================================================

function inicializarIndicadorForca() {
    // Comentário: Obter campo de senha
    const passwordInput = document.getElementById('id_password1');
    
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            calcularForcaSenha(this.value);
        });
    }
}

function calcularForcaSenha(senha) {
    // Comentário: Calcular força da senha
    let forca = 0;
    const strengthBar = document.querySelector('.password-strength');
    const strengthText = document.getElementById('strengthText');
    
    // Comentário: Verificar critérios
    if (senha.length >= 8) forca += 1;
    if (senha.length >= 12) forca += 1;
    if (/[a-z]/.test(senha)) forca += 1;
    if (/[A-Z]/.test(senha)) forca += 1;
    if (/[0-9]/.test(senha)) forca += 1;
    if (/[^a-zA-Z0-9]/.test(senha)) forca += 1;
    
    // Comentário: Remover classes anteriores
    strengthBar.classList.remove('strength-weak', 'strength-medium', 'strength-strong');
    
    // Comentário: Aplicar classe baseada na força
    if (forca <= 2) {
        strengthBar.classList.add('strength-weak');
        strengthText.textContent = 'Fraca';
    } else if (forca <= 4) {
        strengthBar.classList.add('strength-medium');
        strengthText.textContent = 'Média';
    } else {
        strengthBar.classList.add('strength-strong');
        strengthText.textContent = 'Forte';
    }
}

// ============================================================
// SEÇÃO 6: TOGGLE DE VISIBILIDADE DE SENHA
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
// SEÇÃO 7: NOTIFICAÇÕES
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

console.log('✅ Todos os scripts de cadastro seguro inicializados com sucesso!');
