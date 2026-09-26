/* ============================================================ */
/* ARQUIVO: painel.js */
/* DESCRIÇÃO: JavaScript para o painel do cliente */
/* IDIOMA: Português */
/* ============================================================ */

/* ============================================================ */
/* SEÇÃO 1: INICIALIZAÇÃO */
/* ============================================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Comentário: Inicializar carrossel de imagens
    inicializarCarrossel();
    
    // Comentário: Inicializar interações da tabela
    inicializarTabelaAgendamentos();
    
    // Comentário: Inicializar animações dos cards
    inicializarAnimacoes();
    
    // Comentário: Inicializar ações rápidas
    inicializarAcoesRapidas();
    
    console.log('Painel do cliente inicializado com sucesso!');
});

/* ============================================================ */
/* SEÇÃO 2: CARROSSEL DE IMAGENS */
/* ============================================================ */

let indiceSlideAtual = 0;
let intervaloCarrossel = null;

function inicializarCarrossel() {
    // Comentário: Obter elementos do carrossel
    const slides = document.querySelectorAll('.carousel-slide');
    const indicadores = document.querySelectorAll('.indicator');
    
    // Comentário: Verificar se existem slides
    if (slides.length === 0) {
        console.warn('Nenhum slide encontrado no carrossel');
        return;
    }
    
    // Comentário: Iniciar rotação automática
    iniciarRotacaoAutomatica(slides, indicadores);
    
    // Comentário: Adicionar eventos aos indicadores
    indicadores.forEach((indicador, indice) => {
        indicador.addEventListener('click', function() {
            // Comentário: Parar rotação automática
            clearInterval(intervaloCarrossel);
            
            // Comentário: Mostrar slide selecionado
            mostrarSlide(indice, slides, indicadores);
            
            // Comentário: Reiniciar rotação automática
            iniciarRotacaoAutomatica(slides, indicadores);
        });
    });
    
    // Comentário: Pausar rotação ao passar o mouse
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', function() {
            clearInterval(intervaloCarrossel);
        });
        
        carouselContainer.addEventListener('mouseleave', function() {
            iniciarRotacaoAutomatica(slides, indicadores);
        });
    }
}

function iniciarRotacaoAutomatica(slides, indicadores) {
    // Comentário: Rotacionar slides a cada 5 segundos
    intervaloCarrossel = setInterval(() => {
        // Comentário: Incrementar índice
        indiceSlideAtual = (indiceSlideAtual + 1) % slides.length;
        
        // Comentário: Mostrar próximo slide
        mostrarSlide(indiceSlideAtual, slides, indicadores);
    }, 5000);
}

function mostrarSlide(indice, slides, indicadores) {
    // Comentário: Remover classe ativa de todos os slides
    slides.forEach(slide => {
        slide.classList.remove('active');
    });
    
    // Comentário: Remover classe ativa de todos os indicadores
    indicadores.forEach(indicador => {
        indicador.classList.remove('active');
    });
    
    // Comentário: Adicionar classe ativa ao slide selecionado
    slides[indice].classList.add('active');
    
    // Comentário: Adicionar classe ativa ao indicador selecionado
    indicadores[indice].classList.add('active');
    
    // Comentário: Atualizar índice atual
    indiceSlideAtual = indice;
}

/* ============================================================ */
/* SEÇÃO 3: TABELA DE AGENDAMENTOS */
/* ============================================================ */

function inicializarTabelaAgendamentos() {
    // Comentário: Obter todas as linhas da tabela
    const linhasTabela = document.querySelectorAll('.appointment-row');
    
    linhasTabela.forEach(linha => {
        // Comentário: Adicionar evento de hover
        linha.addEventListener('mouseenter', function() {
            // Comentário: Adicionar efeito visual
            this.style.backgroundColor = 'rgba(255, 107, 0, 0.05)';
        });
        
        linha.addEventListener('mouseleave', function() {
            // Comentário: Remover efeito visual
            this.style.backgroundColor = '';
        });
        
        // Comentário: Adicionar evento de clique
        linha.addEventListener('click', function() {
            // Comentário: Obter ID do agendamento
            const idAgendamento = this.getAttribute('data-id');
            console.log('Agendamento selecionado:', idAgendamento);
        });
    });
    
    // Comentário: Adicionar eventos aos botões de ação
    const botoesEditar = document.querySelectorAll('.btn-edit');
    botoesEditar.forEach(botao => {
        botao.addEventListener('click', function(e) {
            e.preventDefault();
            const linha = this.closest('.appointment-row');
            const idAgendamento = linha.getAttribute('data-id');
            console.log('Editar agendamento:', idAgendamento);
            // TODO: Implementar lógica de edição
        });
    });
}

/* ============================================================ */
/* SEÇÃO 4: ANIMAÇÕES DOS CARDS */
/* ============================================================ */

function inicializarAnimacoes() {
    // Comentário: Animar cards de estatísticas
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, indice) => {
        // Comentário: Usar Intersection Observer para animar quando visível
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Comentário: Adicionar classe de animação
                    card.style.animation = `slideInUp 0.5s ease-in-out ${indice * 0.1}s forwards`;
                    
                    // Comentário: Animar a barra de progresso
                    const statBar = card.querySelector('.stat-bar::after');
                    if (statBar) {
                        card.querySelector('.stat-bar').style.animation = `growBar 1.5s ease-in-out ${indice * 0.1}s forwards`;
                    }
                    
                    // Comentário: Parar de observar
                    observer.unobserve(card);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(card);
    });
}

/* ============================================================ */
/* SEÇÃO 5: AÇÕES RÁPIDAS */
/* ============================================================ */

function inicializarAcoesRapidas() {
    // Comentário: Obter todos os botões de ação rápida
    const acoesRapidas = document.querySelectorAll('.quick-action');
    
    acoesRapidas.forEach(acao => {
        // Comentário: Adicionar evento de clique
        acao.addEventListener('click', function(e) {
            // Comentário: Obter URL do link
            const url = this.getAttribute('href');
            console.log('Ação rápida:', url);
        });
        
        // Comentário: Adicionar efeito de ripple
        acao.addEventListener('mousedown', function(e) {
            // Comentário: Criar elemento de ripple
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 107, 0, 0.5)';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.animation = 'ripple 0.6s ease-out';
            
            // Comentário: Adicionar ao elemento
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            // Comentário: Remover ripple após animação
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

/* ============================================================ */
/* SEÇÃO 6: FUNÇÕES AUXILIARES */
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
    // Comentário: Criar elemento de toast
    const toast = document.createElement('div');
    toast.className = `alerta alerta-${tipo}`;
    toast.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${mensagem}</span>
        <button type="button" class="botao-fechar-alerta">&times;</button>
    `;
    
    // Comentário: Adicionar ao DOM
    const container = document.querySelector('.container-mensagens') || document.body;
    container.appendChild(toast);
    
    // Comentário: Fechar após 5 segundos
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/* ============================================================ */
/* SEÇÃO 7: ANIMAÇÕES CSS ADICIONAIS */
/* ============================================================ */

// Comentário: Adicionar estilos de animação dinamicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes growBar {
        to {
            width: 100%;
        }
    }
`;
document.head.appendChild(style);

/* ============================================================ */
/* SEÇÃO 8: MONITORAMENTO DE PERFORMANCE */
/* ============================================================ */

function monitorarPerformance() {
    // Comentário: Registrar tempo de carregamento
    window.addEventListener('load', function() {
        // Comentário: Obter informações de performance
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        
        console.log('Tempo de carregamento da página:', pageLoadTime + 'ms');
    });
}

// Comentário: Chamar função de monitoramento
monitorarPerformance();

/* ============================================================ */
/* FIM DO ARQUIVO */
/* ============================================================ */
