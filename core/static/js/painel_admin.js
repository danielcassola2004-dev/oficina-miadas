/* ============================================================
   ARQUIVO: painel_admin_updated.js
   DESCRIÇÃO: JavaScript para novos status de agendamentos
   IDIOMA: Português
   ============================================================ */

// ============================================================
// SEÇÃO 1: INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Script do painel admin atualizado carregado');
    
    // Comentário: Inicializar funcionalidades
    inicializarBotoes();
    inicializarAnimacoes();
    inicializarConfirmacoes();
});

// ============================================================
// SEÇÃO 2: INICIALIZAR BOTÕES
// ============================================================

function inicializarBotoes() {
    // Comentário: Adicionar eventos aos botões de ação
    const botoes = document.querySelectorAll('.btn-icon');
    
    botoes.forEach(botao => {
        // Comentário: Efeito ripple ao clicar
        botao.addEventListener('click', function(e) {
            // Comentário: Criar elemento de ripple
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            // Comentário: Remover ripple após animação
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Comentário: Adicionar eventos aos botões de sucesso (Atendido)
    const botoesSuccess = document.querySelectorAll('.btn-icon.success');
    botoesSuccess.forEach(botao => {
        botao.addEventListener('mouseenter', function() {
            console.log('Marcar como Atendido');
        });
    });
    
    // Comentário: Adicionar eventos aos botões de aviso (Não Compareceu)
    const botoesWarning = document.querySelectorAll('.btn-icon.warning');
    botoesWarning.forEach(botao => {
        botao.addEventListener('mouseenter', function() {
            console.log('Marcar como Não Compareceu');
        });
    });
}

// ============================================================
// SEÇÃO 3: INICIALIZAR ANIMAÇÕES
// ============================================================

function inicializarAnimacoes() {
    // Comentário: Animar linhas da tabela ao carregar
    const linhas = document.querySelectorAll('.appointment-row');
    
    linhas.forEach((linha, index) => {
        linha.style.opacity = '0';
        linha.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            linha.style.transition = 'all 0.3s ease';
            linha.style.opacity = '1';
            linha.style.transform = 'translateY(0)';
        }, index * 50);
    });
    
    // Comentário: Destacar linhas expiradas
    const linhasExpiradas = document.querySelectorAll('.appointment-row[data-status="expirado"]');
    linhasExpiradas.forEach(linha => {
        linha.classList.add('status-expirado');
    });
}

// ============================================================
// SEÇÃO 4: CONFIRMAÇÕES
// ============================================================

function inicializarConfirmacoes() {
    // Comentário: Adicionar confirmação aos botões de perigo
    const botoesDanger = document.querySelectorAll('.btn-icon.danger');
    
    botoesDanger.forEach(botao => {
        botao.addEventListener('click', function(e) {
            if (!confirm('Tem a certeza que deseja cancelar este agendamento?')) {
                e.preventDefault();
            }
        });
    });
    
    // Comentário: Adicionar confirmação aos botões de sucesso
    const botoesSuccess = document.querySelectorAll('.btn-icon.success');
    
    botoesSuccess.forEach(botao => {
        botao.addEventListener('click', function(e) {
            if (!confirm('Tem a certeza que deseja marcar este agendamento como atendido?')) {
                e.preventDefault();
            }
        });
    });
    
    // Comentário: Adicionar confirmação aos botões de aviso
    const botoesWarning = document.querySelectorAll('.btn-icon.warning');
    
    botoesWarning.forEach(botao => {
        botao.addEventListener('click', function(e) {
            if (!confirm('Tem a certeza que deseja marcar este agendamento como não comparecido?')) {
                e.preventDefault();
            }
        });
    });
}

// ============================================================
// SEÇÃO 5: ATUALIZAR TABELA EM TEMPO REAL
// ============================================================

function atualizarTabelaEmTempoReal() {
    // Comentário: Atualizar tabela a cada 30 segundos
    setInterval(function() {
        console.log('Atualizando tabela de agendamentos...');
        
        // Comentário: Aqui você pode fazer uma requisição AJAX para atualizar os dados
        // fetch('/api/agendamentos/')
        //     .then(response => response.json())
        //     .then(data => {
        //         // Atualizar tabela com novos dados
        //     });
    }, 30000); // 30 segundos
}

// ============================================================
// SEÇÃO 6: NOTIFICAÇÕES
// ============================================================

function mostrarNotificacao(mensagem, tipo = 'sucesso') {
    // Comentário: Mostrar notificação no topo da página
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
// SEÇÃO 7: FILTRAR AGENDAMENTOS
// ============================================================

function filtrarAgendamentos(status) {
    // Comentário: Filtrar agendamentos por status
    const linhas = document.querySelectorAll('.appointment-row');
    
    linhas.forEach(linha => {
        if (status === 'todos' || linha.getAttribute('data-status') === status) {
            linha.style.display = '';
            linha.style.opacity = '1';
        } else {
            linha.style.display = 'none';
            linha.style.opacity = '0.5';
        }
    });
}

// ============================================================
// SEÇÃO 8: EXPORTAR DADOS
// ============================================================

function exportarParaCSV() {
    // Comentário: Exportar tabela para CSV
    const tabela = document.querySelector('.table');
    let csv = '';
    
    // Comentário: Adicionar cabeçalhos
    const headers = tabela.querySelectorAll('thead th');
    headers.forEach(header => {
        csv += header.textContent + ',';
    });
    csv += '\n';
    
    // Comentário: Adicionar linhas
    const linhas = tabela.querySelectorAll('tbody tr');
    linhas.forEach(linha => {
        const colunas = linha.querySelectorAll('td');
        colunas.forEach(coluna => {
            csv += coluna.textContent + ',';
        });
        csv += '\n';
    });
    
    // Comentário: Criar arquivo e fazer download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'agendamentos.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// ============================================================
// SEÇÃO 9: ESTILOS DINÂMICOS
// ============================================================

// Comentário: Adicionar estilos dinâmicos para animações
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
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('✅ Todos os scripts do painel admin atualizado inicializados com sucesso!');
