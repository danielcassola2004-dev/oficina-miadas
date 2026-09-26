/* ============================================================ */
/* ARQUIVO: base_home.js */
/* DESCRIÇÃO: JavaScript para a base do cliente */
/* IDIOMA: Português */
/* ============================================================ */

/* ============================================================ */
/* SEÇÃO 1: INICIALIZAÇÃO */
/* ============================================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tema
    inicializarTema();
    
    // Inicializar sidebar
    inicializarSidebar();
    
    // Inicializar alertas
    inicializarAlertas();
    
    // Carregar notificações
    carregarNotificacoes();
    
    // Atualizar notificações a cada 30 segundos
    setInterval(carregarNotificacoes, 30000);
    
    console.log('Base do cliente inicializada com sucesso!');
});

/* ============================================================ */
/* SEÇÃO 2: GERENCIAMENTO DE TEMA */
/* ============================================================ */

function inicializarTema() {
    // Comentário: Verificar se há tema salvo no localStorage
    const temaSalvo = localStorage.getItem('tema-cliente');
    
    if (temaSalvo === 'escuro') {
        // Comentário: Ativar tema escuro
        document.body.classList.add('tema-escuro');
        atualizarIconeTema(true);
    } else {
        // Comentário: Manter tema claro
        document.body.classList.remove('tema-escuro');
        atualizarIconeTema(false);
    }
    
    // Comentário: Adicionar evento ao botão de tema
    const botaoTema = document.getElementById('botao-tema');
    if (botaoTema) {
        botaoTema.addEventListener('click', alternarTema);
    }
}

function alternarTema() {
    // Comentário: Alternar classe de tema escuro
    document.body.classList.toggle('tema-escuro');
    
    // Comentário: Verificar se tema escuro está ativo
    const temaEscuroAtivo = document.body.classList.contains('tema-escuro');
    
    // Comentário: Salvar preferência no localStorage
    localStorage.setItem('tema-cliente', temaEscuroAtivo ? 'escuro' : 'claro');
    
    // Comentário: Atualizar ícone
    atualizarIconeTema(temaEscuroAtivo);
}

function atualizarIconeTema(estaEscuro) {
    // Comentário: Atualizar ícone do botão de tema
    const botaoTema = document.getElementById('botao-tema');
    if (botaoTema) {
        const icone = botaoTema.querySelector('i');
        if (icone) {
            icone.className = estaEscuro ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
}

/* ============================================================ */
/* SEÇÃO 3: GERENCIAMENTO DE SIDEBAR */
/* ============================================================ */

function inicializarSidebar() {
    // Comentário: Obter elementos da sidebar
    const botaoToggle = document.getElementById('botao-toggle-sidebar');
    const botaoFechar = document.getElementById('botao-fechar-sidebar');
    const sidebar = document.getElementById('barra-lateral');
    const overlay = document.getElementById('overlay-sidebar');
    
    // Comentário: Adicionar eventos ao botão de toggle
    if (botaoToggle) {
        botaoToggle.addEventListener('click', function() {
            abrirSidebar();
        });
    }
    
    // Comentário: Adicionar eventos ao botão de fechar
    if (botaoFechar) {
        botaoFechar.addEventListener('click', function() {
            fecharSidebar();
        });
    }
    
    // Comentário: Fechar sidebar ao clicar no overlay
    if (overlay) {
        overlay.addEventListener('click', function() {
            fecharSidebar();
        });
    }
    
    // Comentário: Fechar sidebar em mobile ao clicar em um item
    const itensMenu = document.querySelectorAll('.item-menu');
    itensMenu.forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                fecharSidebar();
            }
        });
    });
}

function abrirSidebar() {
    // Comentário: Adicionar classe ativa à sidebar
    const sidebar = document.getElementById('barra-lateral');
    const overlay = document.getElementById('overlay-sidebar');
    
    if (sidebar) {
        sidebar.classList.add('ativa');
    }
    if (overlay) {
        overlay.classList.add('ativo');
    }
}

function fecharSidebar() {
    // Comentário: Remover classe ativa da sidebar
    const sidebar = document.getElementById('barra-lateral');
    const overlay = document.getElementById('overlay-sidebar');
    
    if (sidebar) {
        sidebar.classList.remove('ativa');
    }
    if (overlay) {
        overlay.classList.remove('ativo');
    }
}

/* ============================================================ */
/* SEÇÃO 4: GERENCIAMENTO DE ALERTAS */
/* ============================================================ */

function inicializarAlertas() {
    // Comentário: Obter todos os alertas
    const alertas = document.querySelectorAll('.alerta');
    
    alertas.forEach(alerta => {
        // Comentário: Adicionar evento ao botão de fechar
        const botaoFechar = alerta.querySelector('.botao-fechar-alerta');
        if (botaoFechar) {
            botaoFechar.addEventListener('click', function() {
                fecharAlerta(alerta);
            });
        }
        
        // Comentário: Fechar alerta automaticamente após 5 segundos
        setTimeout(() => {
            fecharAlerta(alerta);
        }, 5000);
    });
}

function fecharAlerta(alerta) {
    // Comentário: Remover alerta com animação
    alerta.style.animation = 'slideInDown 0.3s ease-in-out reverse';
    
    setTimeout(() => {
        alerta.remove();
    }, 300);
}

/* ============================================================ */
/* SEÇÃO 5: CARREGAR NOTIFICAÇÕES */
/* ============================================================ */

function carregarNotificacoes() {
    // Comentário: Fazer requisição AJAX para carregar notificações
    fetch('/api/notificacoes/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Comentário: Atualizar badge de notificações
        const badge = document.getElementById('badge-notificacoes');
        if (badge) {
            badge.textContent = data.nao_lidas || 0;
            
            // Comentário: Mostrar ou esconder badge
            if (data.nao_lidas > 0) {
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    })
    .catch(error => {
        console.error('Erro ao carregar notificações:', error);
    });
}

/* ============================================================ */
/* SEÇÃO 6: MARCAR ITEM ATIVO */
/* ============================================================ */

function marcarItemAtivoSidebar() {
    // Comentário: Obter URL atual
    const urlAtual = window.location.pathname;
    
    // Comentário: Obter todos os itens do menu
    const itensMenu = document.querySelectorAll('.item-menu');
    
    itensMenu.forEach(item => {
        // Comentário: Remover classe ativa
        item.classList.remove('ativo');
        
        // Comentário: Verificar se URL corresponde
        const href = item.getAttribute('href');
        if (href === urlAtual) {
            item.classList.add('ativo');
        }
    });
}

// Comentário: Chamar função ao carregar a página
document.addEventListener('DOMContentLoaded', marcarItemAtivoSidebar);

/* ============================================================ */
/* SEÇÃO 7: BUSCA */
/* ============================================================ */

function inicializarBusca() {
    // Comentário: Obter input de busca
    const inputBusca = document.querySelector('.input-busca');
    
    if (inputBusca) {
        inputBusca.addEventListener('keypress', function(event) {
            // Comentário: Verificar se tecla pressionada é Enter
            if (event.key === 'Enter') {
                // Comentário: Fazer busca
                const termo = this.value;
                console.log('Buscando:', termo);
                // TODO: Implementar lógica de busca
            }
        });
    }
}

// Comentário: Chamar função ao carregar a página
document.addEventListener('DOMContentLoaded', inicializarBusca);

/* ============================================================ */
/* SEÇÃO 8: FUNÇÕES AUXILIARES */
/* ============================================================ */

function formatarData(data) {
    // Comentário: Formatar data em formato legível
    const opcoes = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return new Date(data).toLocaleDateString('pt-PT', opcoes);
}

function mostrarToast(mensagem, tipo = 'info') {
    // Comentário: Criar e mostrar toast
    const toast = document.createElement('div');
    toast.className = `alerta alerta-${tipo}`;
    toast.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${mensagem}</span>
        <button type="button" class="botao-fechar-alerta">&times;</button>
    `;
    
    // Comentário: Adicionar ao container de mensagens
    const container = document.querySelector('.container-mensagens') || document.body;
    container.appendChild(toast);
    
    // Comentário: Fechar após 5 segundos
    setTimeout(() => {
        fecharAlerta(toast);
    }, 5000);
}

/* ============================================================ */
/* FIM DO ARQUIVO */
/* ============================================================ */
