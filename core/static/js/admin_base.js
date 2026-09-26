/* ============================================================
   ARQUIVO: admin_base.js
   DESCRIÇÃO: JavaScript para o painel administrativo
   IDIOMA: Português
   ============================================================ */

// ============================================================
// SEÇÃO 1: INICIALIZAÇÃO - Executa ao carregar a página
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    // Carregar tema salvo
    carregarTema();
    
    // Carregar notificações e emails
    carregarNotificacoes();
    carregarEmails();
    
    // Atualizar notificações a cada 10 segundos
    setInterval(carregarNotificacoes, 10000);
    
    // Atualizar emails a cada 15 segundos
    setInterval(carregarEmails, 15000);
    
    // Configurar event listeners (cliques, etc)
    configurarEventListeners();
});

// ============================================================
// SEÇÃO 2: GERENCIAMENTO DE TEMA (ESCURO/CLARO)
// ============================================================

function carregarTema() {
    // Obter tema do localStorage ou usar "claro" como padrão
    const temaSalvo = localStorage.getItem('tema') || 'claro';
    document.body.setAttribute('data-tema', temaSalvo);
    
    // Atualizar ícone do botão
    atualizarIconeTema(temaSalvo);
}

function alternarTema() {
    // Obter tema atual
    const temaAtual = document.body.getAttribute('data-tema');
    
    // Alternar entre claro e escuro
    const novoTema = temaAtual === 'claro' ? 'escuro' : 'claro';
    
    // Aplicar novo tema
    document.body.setAttribute('data-tema', novoTema);
    
    // Salvar no localStorage
    localStorage.setItem('tema', novoTema);
    
    // Atualizar ícone
    atualizarIconeTema(novoTema);
}

function atualizarIconeTema(tema) {
    // Atualizar ícone do botão de tema
    const botaoTema = document.getElementById('botao-alternar-tema');
    if (botaoTema) {
        const icone = botaoTema.querySelector('i');
        if (icone) {
            // Se tema é claro, mostrar ícone de lua (para escurecer)
            // Se tema é escuro, mostrar ícone de sol (para clarear)
            icone.className = tema === 'claro' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }
}

// ============================================================
// SEÇÃO 3: CARREGAR NOTIFICAÇÕES
// ============================================================

function carregarNotificacoes() {
    // Fazer requisição para API de notificações
    fetch('/api/notificacoes/')
        .then(resposta => resposta.json())
        .then(dados => {
            // Atualizar badge (número de notificações não lidas)
            const badgeNotificacoes = document.getElementById('badge-notificacoes');
            if (badgeNotificacoes) {
                badgeNotificacoes.textContent = dados.nao_lidas || 0;
            }
            
            // Atualizar lista de notificações
            const listaNotificacoes = document.getElementById('lista-notificacoes');
            if (listaNotificacoes) {
                if (dados.notificacoes && dados.notificacoes.length > 0) {
                    // Gerar HTML para cada notificação
                    listaNotificacoes.innerHTML = dados.notificacoes.map(notif => `
                        <div class="item-notificacao ${notif.lida ? 'lida' : 'nao-lida'}">
                            <div class="conteudo-notificacao">
                                <h4>${notif.titulo}</h4>
                                <p>${notif.mensagem}</p>
                                <small>${formatarData(notif.criada_em)}</small>
                            </div>
                            <button onclick="deletarNotificacao(${notif.id})" class="botao-deletar">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `).join('');
                } else {
                    // Mostrar mensagem vazia
                    listaNotificacoes.innerHTML = '<p class="mensagem-vazia">Nenhuma notificação</p>';
                }
            }
        })
        .catch(erro => console.error('Erro ao carregar notificações:', erro));
}

// ============================================================
// SEÇÃO 4: CARREGAR EMAILS
// ============================================================

function carregarEmails() {
    // Fazer requisição para API de emails
    fetch('/api/emails/')
        .then(resposta => resposta.json())
        .then(dados => {
            // Atualizar badge (número de emails não lidos)
            const badgeEmails = document.getElementById('badge-emails');
            if (badgeEmails) {
                badgeEmails.textContent = dados.nao_lidos || 0;
            }
            
            // Atualizar lista de emails
            const listaEmails = document.getElementById('lista-emails');
            if (listaEmails) {
                if (dados.emails && dados.emails.length > 0) {
                    // Gerar HTML para cada email
                    listaEmails.innerHTML = dados.emails.map(email => `
                        <div class="item-email ${email.lido ? 'lido' : 'nao-lido'}">
                            <div class="conteudo-email">
                                <h4>${email.assunto}</h4>
                                <p>${email.remetente}</p>
                                <small>${formatarData(email.criado_em)}</small>
                            </div>
                            <button onclick="deletarEmail(${email.id})" class="botao-deletar">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `).join('');
                } else {
                    // Mostrar mensagem vazia
                    listaEmails.innerHTML = '<p class="mensagem-vazia">Nenhum email</p>';
                }
            }
        })
        .catch(erro => console.error('Erro ao carregar emails:', erro));
}

// ============================================================
// SEÇÃO 5: DELETAR NOTIFICAÇÃO
// ============================================================

function deletarNotificacao(id) {
    // Fazer requisição DELETE para remover notificação
    fetch(`/api/notificacao/${id}/deletar/`, {
        method: 'POST',
        headers: {
            // Obter token CSRF do formulário
            'X-CSRFToken': obterTokenCSRF()
        }
    })
    .then(resposta => resposta.json())
    .then(dados => {
        if (dados.sucesso) {
            // Recarregar notificações
            carregarNotificacoes();
        }
    })
    .catch(erro => console.error('Erro ao deletar notificação:', erro));
}

// ============================================================
// SEÇÃO 6: DELETAR EMAIL
// ============================================================

function deletarEmail(id) {
    // Fazer requisição DELETE para remover email
    fetch(`/api/email/${id}/deletar/`, {
        method: 'POST',
        headers: {
            // Obter token CSRF do formulário
            'X-CSRFToken': obterTokenCSRF()
        }
    })
    .then(resposta => resposta.json())
    .then(dados => {
        if (dados.sucesso) {
            // Recarregar emails
            carregarEmails();
        }
    })
    .catch(erro => console.error('Erro ao deletar email:', erro));
}

// ============================================================
// SEÇÃO 7: FORMATAR DATA
// ============================================================

function formatarData(dataString) {
    // Converter string para objeto Date
    const data = new Date(dataString);
    const hoje = new Date();
    
    // Calcular diferença em milissegundos
    const diferenca = hoje - data;
    
    // Se foi hoje (menos de 24 horas)
    if (diferenca < 86400000) {
        return data.toLocaleTimeString('pt-PT', { hour: '2-digit', minute: '2-digit' });
    }
    
    // Se foi ontem (menos de 48 horas)
    if (diferenca < 172800000) {
        return 'Ontem';
    }
    
    // Caso contrário, mostrar data
    return data.toLocaleDateString('pt-PT');
}

// ============================================================
// SEÇÃO 8: OBTER TOKEN CSRF
// ============================================================

function obterTokenCSRF() {
    // Procurar token CSRF no formulário ou meta tag
    const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                  document.querySelector('meta[name="csrf-token"]')?.content || '';
    return token;
}

// ============================================================
// SEÇÃO 9: CONFIGURAR EVENT LISTENERS
// ============================================================

function configurarEventListeners() {
    // ========== BOTÃO ALTERNAR TEMA ==========
    const botaoTema = document.getElementById('botao-alternar-tema');
    if (botaoTema) {
        botaoTema.addEventListener('click', alternarTema);
    }
    
    // ========== BOTÃO NOTIFICAÇÕES ==========
    const botaoNotificacoes = document.getElementById('botao-notificacoes');
    if (botaoNotificacoes) {
        botaoNotificacoes.addEventListener('click', function(evento) {
            // Evitar que o evento se propague
            evento.stopPropagation();
            
            // Obter dropdowns
            const dropdownNotificacoes = document.getElementById('dropdown-notificacoes');
            const dropdownEmails = document.getElementById('dropdown-emails');
            
            // Alternar visibilidade do dropdown de notificações
            if (dropdownNotificacoes) {
                const estaVisivel = dropdownNotificacoes.style.display === 'block';
                dropdownNotificacoes.style.display = estaVisivel ? 'none' : 'block';
            }
            
            // Fechar dropdown de emails
            if (dropdownEmails) {
                dropdownEmails.style.display = 'none';
            }
        });
    }
    
    // ========== BOTÃO EMAILS ==========
    const botaoEmails = document.getElementById('botao-emails');
    if (botaoEmails) {
        botaoEmails.addEventListener('click', function(evento) {
            // Evitar que o evento se propague
            evento.stopPropagation();
            
            // Obter dropdowns
            const dropdownEmails = document.getElementById('dropdown-emails');
            const dropdownNotificacoes = document.getElementById('dropdown-notificacoes');
            
            // Alternar visibilidade do dropdown de emails
            if (dropdownEmails) {
                const estaVisivel = dropdownEmails.style.display === 'block';
                dropdownEmails.style.display = estaVisivel ? 'none' : 'block';
            }
            
            // Fechar dropdown de notificações
            if (dropdownNotificacoes) {
                dropdownNotificacoes.style.display = 'none';
            }
        });
    }
    
    // ========== BOTÃO FECHAR NOTIFICAÇÕES ==========
    const botaoFecharNotificacoes = document.getElementById('botao-fechar-notificacoes');
    if (botaoFecharNotificacoes) {
        botaoFecharNotificacoes.addEventListener('click', function() {
            const dropdown = document.getElementById('dropdown-notificacoes');
            if (dropdown) {
                dropdown.style.display = 'none';
            }
        });
    }
    
    // ========== BOTÃO FECHAR EMAILS ==========
    const botaoFecharEmails = document.getElementById('botao-fechar-emails');
    if (botaoFecharEmails) {
        botaoFecharEmails.addEventListener('click', function() {
            const dropdown = document.getElementById('dropdown-emails');
            if (dropdown) {
                dropdown.style.display = 'none';
            }
        });
    }
    
    // ========== BOTÃO MENU UTILIZADOR ==========
    const botaoUtilizador = document.getElementById('botao-utilizador');
    if (botaoUtilizador) {
        botaoUtilizador.addEventListener('click', function(evento) {
            evento.stopPropagation();
            const dropdown = document.getElementById('dropdown-utilizador');
            if (dropdown) {
                const estaVisivel = dropdown.style.display === 'block';
                dropdown.style.display = estaVisivel ? 'none' : 'block';
            }
        });
    }
    
    // ========== FECHAR DROPDOWNS AO CLICAR FORA ==========
    document.addEventListener('click', function(evento) {
        // Se não clicou em notificações, fechar dropdown
        if (!evento.target.closest('.container-notificacoes')) {
            const dropdown = document.getElementById('dropdown-notificacoes');
            if (dropdown) {
                dropdown.style.display = 'none';
            }
        }
        
        // Se não clicou em emails, fechar dropdown
        if (!evento.target.closest('.container-emails')) {
            const dropdown = document.getElementById('dropdown-emails');
            if (dropdown) {
                dropdown.style.display = 'none';
            }
        }
        
        // Se não clicou em menu utilizador, fechar dropdown
        if (!evento.target.closest('.menu-utilizador')) {
            const dropdown = document.getElementById('dropdown-utilizador');
            if (dropdown) {
                dropdown.style.display = 'none';
            }
        }
    });
    
    // ========== FECHAR ALERTAS AUTOMÁTICO ==========
    const alertas = document.querySelectorAll('.alerta');
    alertas.forEach(alerta => {
        // Fechar alerta após 5 segundos
        setTimeout(() => {
            alerta.style.display = 'none';
        }, 5000);
        
        // Fechar alerta ao clicar no botão X
        const botaoFechar = alerta.querySelector('.botao-fechar-alerta');
        if (botaoFechar) {
            botaoFechar.addEventListener('click', function() {
                alerta.style.display = 'none';
            });
        }
    });
}

// ============================================================
// FIM DO ARQUIVO
// ============================================================
