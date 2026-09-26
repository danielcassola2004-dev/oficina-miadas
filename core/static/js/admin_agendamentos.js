/* ============================================================
   ARQUIVO: admin_agendamentos.js
   DESCRIÇÃO: Interatividade do painel de agendamentos
   ============================================================ */

// ============================================================
// SEÇÃO 1: INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar filtros
    inicializarFiltros();
    
    // Inicializar busca
    inicializarBusca();
    
    // Inicializar modal
    inicializarModal();
    
    // Verificar expiração de agendamentos
    verificarExpiracaoAgendamentos();
    
    // Atualizar a cada 5 minutos
    setInterval(verificarExpiracaoAgendamentos, 300000);
});

// ============================================================
// SEÇÃO 2: FILTROS
// ============================================================

function inicializarFiltros() {
    // Comentário: Adicionar event listeners aos botões de filtro
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remover classe active de todos
            filterBtns.forEach(b => b.classList.remove('active'));
            
            // Adicionar classe active ao clicado
            this.classList.add('active');
            
            // Filtrar tabela
            const filter = this.getAttribute('data-filter');
            filtrarTabela(filter);
        });
    });
}

function filtrarTabela(filter) {
    // Comentário: Filtrar linhas da tabela por status
    const rows = document.querySelectorAll('.agendamento-row');
    
    rows.forEach(row => {
        if (filter === 'todos') {
            row.style.display = '';
        } else {
            const status = row.getAttribute('data-status');
            if (status === filter) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

// ============================================================
// SEÇÃO 3: BUSCA
// ============================================================

function inicializarBusca() {
    // Comentário: Adicionar event listener ao input de busca
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            buscarAgendamentos(this.value.toLowerCase());
        });
    }
}

function buscarAgendamentos(termo) {
    // Comentário: Buscar agendamentos por cliente, email ou telefone
    const rows = document.querySelectorAll('.agendamento-row');
    
    rows.forEach(row => {
        const cliente = row.querySelector('.cliente-cell').textContent.toLowerCase();
        const email = row.querySelector('.email-cell').textContent.toLowerCase();
        const telefone = row.querySelector('.telefone-cell')?.textContent.toLowerCase() || '';
        
        if (cliente.includes(termo) || email.includes(termo) || telefone.includes(termo)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// ============================================================
// SEÇÃO 4: AÇÕES DE AGENDAMENTO
// ============================================================

function confirmarAgendamento(id) {
    // Comentário: Confirmar agendamento (apenas se pago)
    if (confirm('Tem certeza que deseja confirmar este agendamento?')) {
        fetch(`/confirmar/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacao('✅ Agendamento confirmado com sucesso!', 'sucesso');
                location.reload();
            } else {
                mostrarNotificacao('❌ Erro ao confirmar agendamento', 'erro');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            mostrarNotificacao('❌ Erro ao confirmar agendamento', 'erro');
        });
    }
}

function iniciarServico(id) {
    // Comentário: Iniciar serviço (mudar status para em_andamento)
    if (confirm('Tem certeza que deseja iniciar este serviço?')) {
        fetch(`/iniciar-servico/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacao('🔄 Serviço iniciado!', 'sucesso');
                location.reload();
            } else {
                mostrarNotificacao('❌ Erro ao iniciar serviço', 'erro');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            mostrarNotificacao('❌ Erro ao iniciar serviço', 'erro');
        });
    }
}

function concluirServico(id) {
    // Comentário: Concluir serviço (mudar status para concluido)
    if (confirm('Tem certeza que deseja concluir este serviço?')) {
        fetch(`/concluir-servico/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacao('✔️ Serviço concluído!', 'sucesso');
                location.reload();
            } else {
                mostrarNotificacao('❌ Erro ao concluir serviço', 'erro');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            mostrarNotificacao('❌ Erro ao concluir serviço', 'erro');
        });
    }
}

function cancelarAgendamento(id) {
    // Comentário: Cancelar agendamento
    if (confirm('Tem certeza que deseja cancelar este agendamento?')) {
        fetch(`/cancelar-admin/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacao('❌ Agendamento cancelado', 'aviso');
                location.reload();
            } else {
                mostrarNotificacao('❌ Erro ao cancelar agendamento', 'erro');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            mostrarNotificacao('❌ Erro ao cancelar agendamento', 'erro');
        });
    }
}

// ============================================================
// SEÇÃO 5: MODAL DE DETALHES
// ============================================================

function inicializarModal() {
    // Comentário: Inicializar modal de detalhes
    const modal = document.getElementById('detalhesModal');
    const closeBtn = document.querySelector('.close');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

function verDetalhes(id) {
    // Comentário: Buscar e exibir detalhes do agendamento
    fetch(`/api/agendamento/${id}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            exibirDetalhesModal(data.agendamento);
        } else {
            mostrarNotificacao('❌ Erro ao carregar detalhes', 'erro');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        mostrarNotificacao('❌ Erro ao carregar detalhes', 'erro');
    });
}

function exibirDetalhesModal(agendamento) {
    // Comentário: Exibir detalhes no modal
    const modal = document.getElementById('detalhesModal');
    const conteudo = document.getElementById('detalhesConteudo');
    
    const html = `
        <div class="detalhes-info">
            <p><strong>ID:</strong> ${agendamento.id}</p>
            <p><strong>Cliente:</strong> ${agendamento.nome}</p>
            <p><strong>Email:</strong> ${agendamento.email}</p>
            <p><strong>Telefone:</strong> ${agendamento.telefone}</p>
            <p><strong>Serviço:</strong> ${agendamento.servico}</p>
            <p><strong>Data:</strong> ${agendamento.data}</p>
            <p><strong>Hora:</strong> ${agendamento.hora}</p>
            <p><strong>Status:</strong> <span class="status-badge status-${agendamento.status}">${agendamento.status_display}</span></p>
            <p><strong>Pagamento:</strong> <span class="pagamento-badge pagamento-${agendamento.status_pagamento}">${agendamento.pagamento_display}</span></p>
            <p><strong>Valor:</strong> ${agendamento.valor} MT</p>
            <p><strong>Observações:</strong> ${agendamento.observacoes || 'Nenhuma'}</p>
        </div>
    `;
    
    conteudo.innerHTML = html;
    modal.style.display = 'block';
}

// ============================================================
// SEÇÃO 6: VERIFICAÇÃO DE EXPIRAÇÃO
// ============================================================

function verificarExpiracaoAgendamentos() {
    // Comentário: Verificar agendamentos expirados
    fetch('/agendamentos/verificar-expiracao/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.expirados > 0) {
            console.log(`${data.expirados} agendamentos marcados como expirados`);
            // Atualizar página se houver expirados
            location.reload();
        }
    })
    .catch(error => console.error('Erro:', error));
}

// ============================================================
// SEÇÃO 7: NOTIFICAÇÕES
// ============================================================

function mostrarNotificacao(mensagem, tipo = 'info') {
    // Comentário: Mostrar notificação temporária
    const notificacao = document.createElement('div');
    notificacao.className = `notificacao notificacao-${tipo}`;
    notificacao.textContent = mensagem;
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${tipo === 'sucesso' ? '#10b981' : tipo === 'erro' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notificacao);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notificacao.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notificacao.remove(), 300);
    }, 3000);
}

// ============================================================
// SEÇÃO 8: UTILITÁRIOS
// ============================================================

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
// SEÇÃO 9: ANIMAÇÕES CSS
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
