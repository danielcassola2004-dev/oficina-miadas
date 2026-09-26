/* ============================================================
   ARQUIVO: pagamento.js
   DESCRIÇÃO: Interatividade da página de pagamento
   ============================================================ */

// ============================================================
// SEÇÃO 1: INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    // Comentário: Inicializar formulário de pagamento
    const formPagamento = document.getElementById('formPagamento');
    
    if (formPagamento) {
        formPagamento.addEventListener('submit', processarPagamento);
    }
    
    // Comentário: Validar seleção de método
    const metodoRadios = document.querySelectorAll('input[name="metodo_pagamento"]');
    metodoRadios.forEach(radio => {
        radio.addEventListener('change', validarFormulario);
    });
    
    // Comentário: Validar checkbox de termos
    const checkboxTermos = document.getElementById('aceitar_termos');
    if (checkboxTermos) {
        checkboxTermos.addEventListener('change', validarFormulario);
    }
});

// ============================================================
// SEÇÃO 2: PROCESSAR PAGAMENTO
// ============================================================

function processarPagamento(event) {
    // Comentário: Processar envio do formulário
    event.preventDefault();
    
    // Comentário: Validar formulário
    if (!validarFormulario()) {
        mostrarErro('Por favor, preencha todos os campos obrigatórios');
        return;
    }
    
    // Comentário: Mostrar modal de processamento
    mostrarModalProcessamento();
    
    // Comentário: Obter dados do formulário
    const formData = new FormData(event.target);
    const agendamentoId = obterAgendamentoId();
    
    // Comentário: Enviar para servidor
    fetch('/api/processar-pagamento/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            agendamento_id: agendamentoId,
            metodo_pagamento: formData.get('metodo_pagamento'),
            valor: obterValorPagamento()
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Comentário: Pagamento bem-sucedido
            setTimeout(() => {
                window.location.href = `/pagamento/sucesso/${agendamentoId}/`;
            }, 2000);
        } else {
            // Comentário: Erro no pagamento
            ocultarModalProcessamento();
            mostrarErro(data.message || 'Erro ao processar pagamento');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        ocultarModalProcessamento();
        mostrarErro('Erro ao processar pagamento. Tente novamente.');
    });
}

// ============================================================
// SEÇÃO 3: VALIDAÇÃO
// ============================================================

function validarFormulario() {
    // Comentário: Validar todos os campos obrigatórios
    const metodoSelecionado = document.querySelector('input[name="metodo_pagamento"]:checked');
    const termosAceitos = document.getElementById('aceitar_termos').checked;
    
    if (!metodoSelecionado) {
        mostrarErro('Por favor, selecione um método de pagamento');
        return false;
    }
    
    if (!termosAceitos) {
        mostrarErro('Por favor, aceite os termos e condições');
        return false;
    }
    
    return true;
}

// ============================================================
// SEÇÃO 4: MODAL DE PROCESSAMENTO
// ============================================================

function mostrarModalProcessamento() {
    // Comentário: Mostrar modal de processamento
    const modal = document.getElementById('modalProcessamento');
    if (modal) {
        modal.style.display = 'block';
    }
    
    // Comentário: Desabilitar botão de confirmação
    const btnConfirmar = document.getElementById('btnConfirmar');
    if (btnConfirmar) {
        btnConfirmar.disabled = true;
    }
}

function ocultarModalProcessamento() {
    // Comentário: Ocultar modal de processamento
    const modal = document.getElementById('modalProcessamento');
    if (modal) {
        modal.style.display = 'none';
    }
    
    // Comentário: Habilitar botão de confirmação
    const btnConfirmar = document.getElementById('btnConfirmar');
    if (btnConfirmar) {
        btnConfirmar.disabled = false;
    }
}

// ============================================================
// SEÇÃO 5: NOTIFICAÇÕES
// ============================================================

function mostrarErro(mensagem) {
    // Comentário: Mostrar mensagem de erro
    const notificacao = document.createElement('div');
    notificacao.className = 'notificacao notificacao-erro';
    notificacao.textContent = '❌ ' + mensagem;
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: #ef4444;
        color: white;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notificacao);
    
    // Comentário: Remover após 5 segundos
    setTimeout(() => {
        notificacao.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notificacao.remove(), 300);
    }, 5000);
}

function mostrarSucesso(mensagem) {
    // Comentário: Mostrar mensagem de sucesso
    const notificacao = document.createElement('div');
    notificacao.className = 'notificacao notificacao-sucesso';
    notificacao.textContent = '✅ ' + mensagem;
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: #10b981;
        color: white;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notificacao);
    
    // Comentário: Remover após 3 segundos
    setTimeout(() => {
        notificacao.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notificacao.remove(), 300);
    }, 3000);
}

// ============================================================
// SEÇÃO 6: UTILITÁRIOS
// ============================================================

function voltarAtras() {
    // Comentário: Voltar para página anterior
    if (confirm('Tem certeza que deseja cancelar o pagamento?')) {
        window.history.back();
    }
}

function obterAgendamentoId() {
    // Comentário: Obter ID do agendamento da URL
    const url = window.location.pathname;
    const match = url.match(/pagamento\/(\d+)/);
    return match ? match[1] : null;
}

function obterValorPagamento() {
    // Comentário: Obter valor do pagamento do resumo
    const valorElement = document.querySelector('.valor-total');
    if (valorElement) {
        const valor = valorElement.textContent.match(/[\d.]+/)[0];
        return parseFloat(valor);
    }
    return 0;
}

function getCookie(name) {
    // Comentário: Obter valor do cookie CSRF
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ============================================================
// SEÇÃO 7: ANIMAÇÕES CSS
// ============================================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
