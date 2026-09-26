# ============================================================
# ARQUIVO: urls.py - ATUALIZADO COM NOVAS ROTAS
# DESCRIÇÃO: Configuração de URLs para a aplicação
# ============================================================

from django.urls import path
from . import views

urlpatterns = [

    # ============================================================
    # SEÇÃO 2: ROTAS PÚBLICAS
    # ============================================================
    
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    

    # ============================================================
    # SEÇÃO 3: ROTAS DO CLIENTE
    # ============================================================
    
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('servicos/', views.servicos, name='servicos'),
    path('agendar/', views.agendar, name='agendar'),
    path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
    path('cancelar/<int:id>/', views.cancelar_agendamento_cliente, name='cancelar_agendamento_cliente'),
    path('publicidades/', views.publicidades_view, name='publicidades'),
    path('notificacao/', views.notificacao_cliente, name='notificacao'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('api/notificacoes/', views.api_notificacoes, name='api_notificacoes'),
    path('api/emails/', views.api_emails, name='api_emails'),
    path('api/notificacao/<int:id>/deletar/', views.api_deletar_notificacao, name='api_deletar_notificacao'),
    path('api/email/<int:id>/deletar/', views.api_deletar_email, name='api_deletar_email'),
    path('chat/', views.chat_cliente, name='chat_cliente'),
    path('chat/enviar/', views.enviar_mensagem_cliente, name='enviar_mensagem_cliente'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
    
    # NOVA ROTA: PDF do Agendamento
    path('agendamento/pdf/<int:agendamento_id>/', views.gerar_pdf_agendamento, name='gerar_pdf_agendamento'),
 
    # ============================================================
    # SEÇÃO 4: ROTAS DO PAINEL ADMINISTRATIVO
    # ============================================================
    
    path('painel/', views.painel_admin, name='painel_admin'),
    path('painel/chat/', views.chat_admin, name='chat_admin'),
    path('painel/chat/enviar/', views.enviar_mensagem_admin, name='enviar_mensagem_admin'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('perfil-admin/', views.perfil_admin, name='admin_perfil'),

    # ============================================================
    # SEÇÃO 5: ROTAS DE SERVIÇOS (ADMIN)
    # ============================================================
    
    path('painel/servicos/', views.admin_servicos, name='admin_servicos'),
    path('painel/servicos/criar/', views.criar_servico, name='criar_servico'),
    path('painel/servicos/editar/<int:id>/', views.editar_servico, name='editar_servico'),
    path('painel/servicos/deletar/<int:id>/', views.deletar_servico, name='deletar_servico'),

    # ============================================================
    # SEÇÃO 6: ROTAS DE AGENDAMENTOS (ADMIN) - ATUALIZADO
    # ============================================================
    
    path('agendamentos/', views.admin_agendamentos, name='admin_agendamentos'),
    path('confirmar/<int:id>/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('cancelar-admin/<int:id>/', views.cancelar_agendamento_admin, name='cancelar_agendamento_admin'),
    
    path('agendamentos/<int:id>/nao-apareceu/', views.marcar_nao_apareceu, name='marcar_nao_apareceu'),
    path('agendamentos/<int:id>/marcar-pago/', views.marcar_pago, name='marcar_pago'),

    # ============================================================
    # SEÇÃO 7: ROTAS DE PUBLICIDADES (ADMIN)
    # ============================================================
    
    path('painel/publicidades/', views.admin_publicidades, name='admin_publicidades'),
    path('painel/publicidades/criar/', views.criar_publicidade, name='criar_publicidade'),
    path('painel/publicidades/editar/<int:id>/', views.editar_publicidade, name='editar_publicidade'),
    path('painel/publicidades/remover/<int:id>/', views.remover_publicidade, name='remover_publicidade'),

    # ============================================================
    # SEÇÃO 8: ROTAS DE RELATÓRIOS (ADMIN)
    # ============================================================
    
    path('painel/relatorio/', views.admin_relatorio, name='admin_relatorio'),
    path('painel/relatorio/exportar/', views.exportar_relatorio, name='exportar_relatorio'),

    # ============================================================
    # SEÇÃO 9: ROTAS DE PAGAMENTO
    # ============================================================
    
    path('pagamento/<int:agendamento_id>/', views.pagina_pagamento, name='pagina_pagamento'),
    path('api/status-pagamento/<int:agendamento_id>/', views.status_pagamento, name='status_pagamento'),
    path('pagamento/sucesso/<int:agendamento_id>/', views.pagamento_sucesso, name='pagamento_sucesso'),
    path('pagamento/erro/<int:agendamento_id>/', views.pagamento_erro, name='pagamento_erro'),

    # ============================================================
    # SEÇÃO 10: ROTAS DE RECUPERAÇÃO DE SENHA
    # ============================================================
    
    path('password-reset/', 
         views.PasswordResetViewCustom.as_view(), 
         name='password_reset'),

    path('password-reset/done/', 
         views.PasswordResetDoneViewCustom.as_view(), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         views.PasswordResetConfirmViewCustom.as_view(), 
         name='password_reset_confirm'),

    path('password-reset/complete/', 
         views.PasswordResetCompleteViewCustom.as_view(), 
         name='password_reset_complete'),
path(
    'exportar-relatorio-pdf/',
    views.exportar_relatorio_pdf,
    name='exportar_relatorio_pdf'
),
path(
    'admin/clientes/detalhes/<int:cliente_id>/',
    views.detalhes_cliente,
    name='detalhes_cliente'
),


path(
    'admin/clientes/remover/<int:cliente_id>/',
    views.remover_cliente,
    name='remover_cliente'
),
]
