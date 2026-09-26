# ============================================================
# ARQUIVO: views.py - REFATORADO COM NOVO SISTEMA DE STATUS
# DESCRIÇÃO: Views com dois status independentes (Confirmação e Pagamento)
# STATUS CONFIRMAÇÃO: Pendente, Confirmado, Cancelado, Não Apareceu
# STATUS PAGAMENTO: Pendente, Pago
# IDIOMA: Português
# ============================================================

# ============================================================
# SEÇÃO 1: IMPORTAÇÕES
# ============================================================

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from django import forms # Adicionado: Importação de forms para PasswordResetViewCustom
import re

from .models import (
    Perfil, Servico, Agendamento, Publicidade, 
    Notificacao, Email, Mensagem
)

# ============================================================
# SEÇÃO 2: FUNÇÕES AUXILIARES
# ============================================================

def is_admin(user):
    """Verifica se o utilizador é administrador"""
    try:
        return user.perfil.tipo == 'ADM'
    except:
        return False


def criar_notificacao(admin, tipo, titulo, mensagem, icone='fas fa-bell', cor='#007bff', agendamento=None, usuario=None):
    """Cria uma notificação no banco de dados"""
    return Notificacao.objects.create(
        admin=admin,
        tipo=tipo,
        titulo=titulo,
        mensagem=mensagem,
        icone=icone,
        cor=cor,
        agendamento=agendamento,
        usuario=usuario
    )


def criar_email(de, email_remetente, assunto, mensagem, prioridade='normal', agendamento=None):
    """Cria um email/mensagem no banco de dados"""
    return Email.objects.create(
        de=de,
        email_remetente=email_remetente,
        assunto=assunto,
        mensagem=mensagem,
        prioridade=prioridade,
        agendamento=agendamento
    )

# ============================================================
# SEÇÃO 3: AUTENTICAÇÃO - LOGIN E CADASTRO
# ============================================================

def index(request):
    """Landing page - Página inicial"""
    publicidades = Publicidade.objects.filter(ativa=True).order_by('-criado_em')[:3]
    servicos = Servico.objects.filter(ativo=True)[:6]
    
    context = {
        'publicidades': publicidades,
        'servicos': servicos,
    }
    return render(request, 'landing/index.html', context)


def login_view(request):
    """Login de utilizador"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Criar notificação de login
            try:
                admin_user = User.objects.filter(perfil__tipo='ADM').first()
                if admin_user:
                    criar_notificacao(
                        admin=admin_user,
                        tipo='sistema',
                        titulo=f'Utilizador {user.username} fez login',
                        mensagem=f'{user.first_name or user.username} acabou de fazer login no sistema',
                        icone='fas fa-sign-in-alt',
                        cor='#28a745',
                        usuario=user
                    )
            except:
                pass
            
            # Redirecionar para dashboard ou admin
            if is_admin(user):
                return redirect('painel_admin')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Utilizador ou senha inválidos')
    
    return render(request, 'landing/login.html')





def cadastro_view(request):
    """Cadastro de novo utilizador com validações completas"""

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        termos = request.POST.get('termos_uso')


        # ==============================
        # VALIDAR NOME DE UTILIZADOR
        # ==============================

        if not username:
            messages.error(request, 'O nome de utilizador é obrigatório.')
            return render(request, 'landing/cadastro.html')


        if len(username) < 3 or len(username) > 20:
            messages.error(
                request,
                'O nome de utilizador deve ter entre 3 e 20 caracteres.'
            )
            return render(request, 'landing/cadastro.html')


        # Impedir nome somente com números
        if not re.search('[a-zA-Z]', username):
            messages.error(
                request,
                'O nome de utilizador deve conter pelo menos uma letra. Números sozinhos não são permitidos.'
            )
            return render(request, 'landing/cadastro.html')


        # Permitir apenas letras, números, _ e -
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            messages.error(
                request,
                'O nome de utilizador contém caracteres inválidos.'
            )
            return render(request, 'landing/cadastro.html')



        # ==============================
        # VALIDAR EMAIL
        # ==============================

        if not email:
            messages.error(request, 'O email é obrigatório.')
            return render(request, 'landing/cadastro.html')


        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Este nome de utilizador já existe.'
            )

            return render(request, 'landing/cadastro.html')



        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Este email já está registado.'
            )

            return render(request, 'landing/cadastro.html')



        # ==============================
        # VALIDAR PASSWORD
        # ==============================

        if password1 != password2:

            messages.error(
                request,
                'As palavras-passe não coincidem.'
            )

            return render(request, 'landing/cadastro.html')



        if len(password1) < 8:

            messages.error(
                request,
                'A palavra-passe deve ter no mínimo 8 caracteres.'
            )

            return render(request, 'landing/cadastro.html')



        # ==============================
        # VALIDAR TERMOS
        # ==============================

        if not termos:

            messages.error(
                request,
                'Deve aceitar os Termos e Condições.'
            )

            return render(request, 'landing/cadastro.html')



        # ==============================
        # CRIAR UTILIZADOR
        # ==============================

        user = User.objects.create_user(

            username=username,

            email=email,

            first_name=username,

            password=password1

        )



        # Criar perfil cliente

        Perfil.objects.create(

            user=user,

            tipo='CLIENTE'

        )



        # ==============================
        # NOTIFICAÇÃO ADMIN
        # ==============================

        try:

            admin_user = User.objects.filter(
                perfil__tipo='ADM'
            ).first()


            if admin_user:

                criar_notificacao(

                    admin=admin_user,

                    tipo='cliente',

                    titulo='Novo Cliente Registado',

                    mensagem=f'{username} acabou de criar uma conta.',

                    icone='fas fa-user-plus',

                    cor='#007bff',

                    usuario=user

                )


                criar_email(

                    de=username,

                    email_remetente=email,

                    assunto='Bem-vindo à Oficina Miadas',

                    mensagem=(
                        f'Olá {username},\n\n'
                        'A sua conta foi criada com sucesso na Oficina Miadas.'
                    ),

                    prioridade='normal'

                )


        except Exception:

            pass



        messages.success(
            request,
            'Conta criada com sucesso! Faça login para continuar.'
        )


        return redirect('login')



    return render(
        request,
        'landing/cadastro.html'
    )

def logout_view(request):
    """Logout de utilizador"""
    logout(request)
    messages.success(request, 'Sessão terminada com sucesso')
    return redirect('index')

# ============================================================
# SEÇÃO 4: ÁREA DO CLIENTE - HOME E DASHBOARD
# ============================================================

@login_required
def home(request):
    """Dashboard do cliente"""

    # Se for administrador vai para painel admin
    if is_admin(request.user):
        return redirect('painel_admin')

    # Buscar agendamentos do cliente logado
    agendamentos = Agendamento.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')


    # Estatísticas do cliente
    total_agendamentos = agendamentos.count()

    confirmados = agendamentos.filter(
        status_confirmacao='confirmado'
    ).count()

    pendentes = agendamentos.filter(
        status_confirmacao='pendente'
    ).count()

    cancelados = agendamentos.filter(
        status_confirmacao='cancelado'
    ).count()


    # Publicidades ativas
    publicidades = Publicidade.objects.filter(
        ativa=True
    ).order_by('-criado_em')[:3]


    # Serviços disponíveis
    servicos = Servico.objects.filter(
        ativo=True
    )


    context = {

        # tabela agendamentos recentes
        'agendamentos': agendamentos[:5],

        # cards estatísticos
        'total_agendamentos': total_agendamentos,
        'confirmados': confirmados,
        'pendentes': pendentes,
        'cancelados': cancelados,

        # outras áreas
        'publicidades': publicidades,
        'servicos': servicos,

    }


    return render(
        request,
        'home/painel.html',
        context
    )

# ============================================================
# SEÇÃO 5: ÁREA DO CLIENTE - SERVIÇOS
# ============================================================

@login_required
def servicos(request):
    """Listagem de serviços para cliente"""
    servicos = Servico.objects.filter(ativo=True)
    
    context = {
        'servicos': servicos,
    }
    return render(request, 'home/servicos.html', context)

# ============================================================
# SEÇÃO 6: ÁREA DO CLIENTE - AGENDAMENTOS COM VALIDAÇÃO
# ============================================================

@login_required
def agendar(request):
    """
    Comentário: Agendar serviço com validações
    - Autenticação obrigatória
    - Data/hora no futuro (mínimo 1 hora)
    - Após agendamento, redireciona para pagamento
    - Status Confirmação: Pendente
    - Status Pagamento: Pendente
    """
    servicos = Servico.objects.filter(ativo=True)
    servico_id = request.GET.get('servico')
    servico_selecionado = None
    
    if servico_id:
        servico_selecionado = get_object_or_404(Servico, id=servico_id)
    
    if request.method == 'POST':
        servico_id = request.POST.get('servico')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        observacoes = request.POST.get('observacoes', '')
        
        # Comentário: Validar data e hora
        try:
            data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora, '%H:%M').time()
            data_hora_agendamento = timezone.make_aware(datetime.combine(data_obj, hora_obj))
            agora = timezone.now()
            
            # Comentário: Verificar se a data/hora está no futuro (mínimo 1 hora)
            diferenca = data_hora_agendamento - agora
            if diferenca.total_seconds() < 3600:  # 1 hora em segundos
                messages.error(request, 'O agendamento deve ser feito com pelo menos 1 hora de antecedência')
                return render(request, 'home/agendar.html', {'servicos': servicos})
        except:
            messages.error(request, 'Data ou hora inválida')
            return render(request, 'home/agendar.html', {'servicos': servicos})
        
        servico = get_object_or_404(Servico, id=servico_id)
        
        # Comentário: Criar agendamento com status pendente (ambos os status)
        agendamento = Agendamento.objects.create(
            usuario=request.user,
            servico=servico,
            nome=request.user.first_name or request.user.username,
            email=request.user.email,
            telefone=request.user.perfil.telefone,
            data=data_obj,
            hora=hora_obj,
            observacoes=observacoes,
            status_confirmacao='pendente',  # NOVO - Status de confirmação
            status_pagamento='pendente',    # NOVO - Status de pagamento
            metodo_pagamento='presencial',  # NOVO - Apenas presencial
            valor_pagamento=servico.preco   # NOVO - Valor do serviço
        )
        
        # Comentário: Criar notificação para admin
        try:
            admin_user = User.objects.filter(perfil__tipo='ADM').first()
            if admin_user:
                criar_notificacao(
                    admin=admin_user,
                    tipo='agendamento',
                    titulo=f'Novo Agendamento - {servico.nome}',
                    mensagem=f'{request.user.first_name or request.user.username} agendou {servico.nome} para {data} às {hora}',
                    icone='fas fa-calendar-check',
                    cor='#28a745',
                    agendamento=agendamento,
                    usuario=request.user
                )
                
                # Comentário: Criar email simulado
                criar_email(
                    de=request.user.first_name or request.user.username,
                    email_remetente=request.user.email,
                    assunto=f'Novo Agendamento - {servico.nome}',
                    mensagem=f'Novo agendamento para {servico.nome} em {data} às {hora}',
                    prioridade='alta',
                    agendamento=agendamento
                )
        except:
            pass
        
        messages.success(request, 'Agendamento realizado! Agora proceda ao pagamento.')
        # Comentário: Redirecionar para página de pagamento
        return redirect('pagina_pagamento', agendamento_id=agendamento.id)
    
    context = {
        'servicos': servicos,
        'servico_selecionado': servico_selecionado,
    }
    return render(request, 'home/agendar.html', context)


@login_required
def meus_agendamentos(request):
    """Listagem de agendamentos do cliente"""
    status_filter = request.GET.get('status', '')
    agendamentos = Agendamento.objects.filter(usuario=request.user)
    
    if status_filter:
        agendamentos = agendamentos.filter(status_confirmacao=status_filter)
        
    agendamentos = agendamentos.order_by('-criado_em')
    
    context = {
        'agendamentos': agendamentos,
        'status_filter': status_filter,
    }
    return render(request, 'home/meus_agendamentos.html', context)


@login_required
@require_POST
def cancelar_agendamento_cliente(request, id):
    """Cancelar agendamento do cliente"""
    agendamento = get_object_or_404(Agendamento, id=id, usuario=request.user)
    
    # Comentário: Permitir cancelamento se pendente ou confirmado
    if agendamento.status_confirmacao in ['pendente', 'confirmado']:
        agendamento.cancelar()
        
        # Criar notificação para admin
        try:
            admin_user = User.objects.filter(perfil__tipo='ADM').first()
            if admin_user:
                criar_notificacao(
                    admin=admin_user,
                    tipo='cancelamento',
                    titulo=f'Agendamento Cancelado',
                    mensagem=f'{request.user.first_name or request.user.username} cancelou o agendamento de {agendamento.servico.nome}',
                    icone='fas fa-times-circle',
                    cor='#dc3545',
                    agendamento=agendamento,
                    usuario=request.user
                )
        except:
            pass
        
        messages.success(request, 'Agendamento cancelado com sucesso')
    else:
        messages.error(request, 'Este agendamento não pode ser cancelado')
    
    return redirect('meus_agendamentos')

# ============================================================
# SEÇÃO 11: PAGAMENTOS
# ============================================================

@login_required
def pagina_pagamento(request, agendamento_id):
    """Regista a opção de pagamento presencial para o agendamento."""
    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id,
        usuario=request.user,
    )

    if request.method == 'POST':
        metodo = request.POST.get('metodo_pagamento')
        confirmar = request.POST.get('aceitar_termos')

        if metodo != 'presencial' or not confirmar:
            messages.error(
                request,
                'Confirme que pretende realizar o pagamento presencial.'
            )
            return redirect('pagina_pagamento', agendamento_id=agendamento.id)

        agendamento.metodo_pagamento = 'presencial'
        agendamento.status_pagamento = 'pendente'
        agendamento.pago_em = None
        agendamento.save(update_fields=[
            'metodo_pagamento',
            'status_pagamento',
            'pago_em',
        ])

        try:
            admin_user = User.objects.filter(perfil__tipo='ADM').first()
            if admin_user:
                criar_notificacao(
                    admin=admin_user,
                    tipo='pagamento',
                    titulo='Pagamento presencial pendente',
                    mensagem=(
                        f'{agendamento.nome} confirmou pagamento presencial '
                        f'para o serviço {agendamento.servico.nome}.'
                    ),
                    icone='fas fa-money-bill-wave',
                    cor='#ff6b00',
                    agendamento=agendamento,
                    usuario=agendamento.usuario,
                )
        except Exception:
            pass

        messages.success(
            request,
            'Pagamento presencial registado. O pagamento será confirmado pela oficina no local.'
        )
        return redirect(
            'pagamento_sucesso',
            agendamento_id=agendamento.id,
        )

    return render(request, 'home/pagamento.html', {'agendamento': agendamento})


@login_required
def pagamento_sucesso(request, agendamento_id):
    """Página de sucesso no pagamento"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    
    context = {
        'agendamento': agendamento,
        'valor': agendamento.valor_pagamento,
        'metodo': agendamento.metodo_pagamento,
    }
    return render(request, 'home/pagamento_sucesso.html', context)


@login_required
def pagamento_erro(request, agendamento_id):
    """Página de erro no pagamento"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    
    context = {
        'agendamento': agendamento,
        'valor': agendamento.valor_pagamento,
    }
    return render(request, 'home/pagamento_erro.html', context)


@login_required
def status_pagamento(request, agendamento_id):
    """Verificar status de pagamento via AJAX"""
    try:
        agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
        
        return JsonResponse({
            'success': True,
            'status_confirmacao': agendamento.status_confirmacao,
            'status_pagamento': agendamento.status_pagamento,
            'metodo_pagamento': agendamento.metodo_pagamento or 'Presencial',
            'valor': str(agendamento.valor_pagamento),
            'data_pagamento': agendamento.pago_em.isoformat() if agendamento.pago_em else None,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# ============================================================
# SEÇÃO 12: PAINEL ADMINISTRATIVO - DASHBOARD
# ============================================================

@login_required
@user_passes_test(is_admin)
def painel_admin(request):
    """Dashboard do admin"""
    agendamentos_total = Agendamento.objects.count()
    agendamentos_confirmados = Agendamento.objects.filter(status_confirmacao='confirmado').count()
    agendamentos_pendentes = Agendamento.objects.filter(status_confirmacao='pendente').count()
    clientes_total = User.objects.filter(perfil__tipo='CLIENTE').count()
    
    receita_total = Agendamento.objects.filter(status_pagamento='pago').aggregate(
        total=Sum('valor_pagamento')
    )['total'] or 0
    
    agendamentos_recentes = Agendamento.objects.all().order_by('-criado_em')[:5]
    notificacoes = Notificacao.objects.filter(admin=request.user, lida=False).order_by('-criada_em')[:5]
    
    context = {
        'agendamentos_total': agendamentos_total,
        'agendamentos_confirmados': agendamentos_confirmados,
        'agendamentos_pendentes': agendamentos_pendentes,
        'clientes_total': clientes_total,
        'receita_total': receita_total,
        'agendamentos_recentes': agendamentos_recentes,
        'notificacoes': notificacoes,
    }
    return render(request, 'admin/painel.html', context)

# ============================================================
# SEÇÃO 13: PAINEL ADMINISTRATIVO - AGENDAMENTOS (NOVO SISTEMA)
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_agendamentos(request):
    """Lista todos os agendamentos com novo sistema de status"""
    status_confirmacao_filter = request.GET.get('status_confirmacao', '')
    status_pagamento_filter = request.GET.get('status_pagamento', '')
    
    agendamentos = Agendamento.objects.all().order_by('-criado_em')
    
    if status_confirmacao_filter:
        agendamentos = agendamentos.filter(status_confirmacao=status_confirmacao_filter)
    
    if status_pagamento_filter:
        agendamentos = agendamentos.filter(status_pagamento=status_pagamento_filter)
    
    total = Agendamento.objects.count()
    pendentes_confirmacao = Agendamento.objects.filter(status_confirmacao='pendente').count()
    confirmados = Agendamento.objects.filter(status_confirmacao='confirmado').count()
    cancelados = Agendamento.objects.filter(status_confirmacao='cancelado').count()
    nao_apareceu = Agendamento.objects.filter(status_confirmacao='nao_apareceu').count()
    
    pendentes_pagamento = Agendamento.objects.filter(status_pagamento='pendente').count()
    pagos = Agendamento.objects.filter(status_pagamento='pago').count()
    
    context = {
        'agendamentos': agendamentos,
        'total': total,
        'pendentes_confirmacao': pendentes_confirmacao,
        'confirmados': confirmados,
        'cancelados': cancelados,
        'nao_apareceu': nao_apareceu,
        'pendentes_pagamento': pendentes_pagamento,
        'pagos': pagos,
        'status_confirmacao_filter': status_confirmacao_filter,
        'status_pagamento_filter': status_pagamento_filter,
    }
    
    return render(request, 'admin/admin_agendamentos.html', context)


@login_required
@user_passes_test(is_admin)
@require_POST
def confirmar_agendamento(request, id):
    """Confirmar agendamento (Pendente → Confirmado)"""
    agendamento = get_object_or_404(Agendamento, id=id)
    
    if not agendamento.pode_confirmar():
        messages.error(request, 'Este agendamento não pode ser confirmado')
        return redirect('admin_agendamentos')
    
    agendamento.confirmar()
    
    try:
        criar_notificacao(
            admin=request.user,
            tipo='confirmacao',
            titulo=f'Agendamento Confirmado',
            mensagem=f'Agendamento de {agendamento.nome} para {agendamento.servico.nome} foi confirmado',
            icone='fas fa-check-circle',
            cor='#28a745',
            agendamento=agendamento,
            usuario=agendamento.usuario
        )
        
        criar_email(
            de='Oficina Miadas',
            email_remetente=settings.DEFAULT_FROM_EMAIL,
            assunto='Seu Agendamento foi Confirmado',
            mensagem=f'Olá {agendamento.nome},\n\nSeu agendamento para {agendamento.servico.nome} em {agendamento.data} às {agendamento.hora} foi confirmado!\n\nObrigado por escolher a Oficina Miadas!',
            prioridade='normal',
            agendamento=agendamento
        )
    except:
        pass
    
    messages.success(request, 'Agendamento confirmado com sucesso')
    return redirect('admin_agendamentos')


@login_required
@user_passes_test(is_admin)
@require_POST
def cancelar_agendamento_admin(request, id):
    """Cancelar agendamento (Confirmado → Cancelado)"""
    agendamento = get_object_or_404(Agendamento, id=id)
    
    if not agendamento.pode_cancelar():
        messages.error(request, 'Este agendamento não pode ser cancelado')
        return redirect('admin_agendamentos')
    
    agendamento.cancelar()
    
    try:
        criar_notificacao(
            admin=request.user,
            tipo='cancelamento',
            titulo=f'Agendamento Cancelado',
            mensagem=f'Agendamento de {agendamento.nome} foi cancelado',
            icone='fas fa-times-circle',
            cor='#dc3545',
            agendamento=agendamento,
            usuario=agendamento.usuario
        )
    except:
        pass
    
    messages.success(request, 'Agendamento cancelado com sucesso')
    return redirect('admin_agendamentos')


@login_required
@user_passes_test(is_admin)
@require_POST
def marcar_nao_apareceu(request, id):
    """Marcar como não apareceu (Confirmado → Não Apareceu)"""
    agendamento = get_object_or_404(Agendamento, id=id)
    
    if not agendamento.pode_marcar_nao_apareceu():
        messages.error(request, 'Este agendamento não pode ser marcado como não apareceu')
        return redirect('admin_agendamentos')
    
    agendamento.marcar_nao_apareceu()
    
    try:
        criar_notificacao(
            admin=request.user,
            tipo='confirmacao',
            titulo=f'Cliente Não Apareceu',
            mensagem=f'{agendamento.nome} não compareceu ao agendamento de {agendamento.servico.nome}',
            icone='fas fa-times-circle',
            cor='#dc3545',
            agendamento=agendamento,
            usuario=agendamento.usuario
        )
    except:
        pass
    
    messages.success(request, 'Agendamento marcado como não apareceu')
    return redirect('admin_agendamentos')


@login_required
@user_passes_test(is_admin)
@require_POST
def marcar_pago(request, id):
    """Marcar pagamento como pago (Pendente → Pago)"""
    agendamento = get_object_or_404(Agendamento, id=id)
    
    if not agendamento.pode_marcar_pago():
        messages.error(request, 'Este agendamento já foi marcado como pago')
        return redirect('admin_agendamentos')
    
    agendamento.marcar_pago()
    
    try:
        criar_notificacao(
            admin=request.user,
            tipo='pagamento',
            titulo=f'Pagamento Marcado como Pago',
            mensagem=f'Pagamento de {agendamento.valor_pagamento} Kz de {agendamento.nome} foi marcado como pago',
            icone='fas fa-money-bill-wave',
            cor='#28a745',
            agendamento=agendamento,
            usuario=agendamento.usuario
        )
    except:
        pass
    
    messages.success(request, 'Pagamento marcado como pago com sucesso')
    return redirect('admin_agendamentos')

# ============================================================
# SEÇÃO 14: PAINEL ADMINISTRATIVO - CLIENTES
# ============================================================

@login_required
@user_passes_test(is_admin)
def lista_clientes(request):
    """Lista de clientes"""
    clientes = User.objects.filter(perfil__tipo='CLIENTE').order_by('-date_joined')
    
    context = {
        'clientes': clientes,
    }
    return render(request, 'admin/clientes.html', context)

# ============================================================
# SEÇÃO 15: PAINEL ADMINISTRATIVO - SERVIÇOS
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_servicos(request):
    """Gestão de serviços"""
    servicos = Servico.objects.all().order_by('nome')
    
    context = {
        'servicos': servicos,
    }
    return render(request, 'admin/admin_servicos.html', context)


@login_required
@user_passes_test(is_admin)
def criar_servico(request):
    """Criar novo serviço"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        preco = request.POST.get('preco')
        imagem = request.FILES.get('imagem')
        ativo = request.POST.get('ativo') == 'on'
        
        servico = Servico.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            imagem=imagem,
            ativo=ativo
        )
        
        criar_notificacao(
            admin=request.user,
            tipo='sistema',
            titulo=f'Novo Serviço Criado',
            mensagem=f'Novo serviço "{nome}" foi adicionado',
            icone='fas fa-plus-circle',
            cor='#28a745'
        )
        
        messages.success(request, 'Serviço criado com sucesso')
        return redirect('admin_servicos')
    
    return render(request, 'admin/servico_form.html', {'form': {'instance': Servico()}})


@login_required
@user_passes_test(is_admin)
def editar_servico(request, id):
    """Editar serviço"""
    servico = get_object_or_404(Servico, id=id)
    
    if request.method == 'POST':
        servico.nome = request.POST.get('nome', servico.nome)
        servico.descricao = request.POST.get('descricao', servico.descricao)
        servico.preco = request.POST.get('preco', servico.preco)
        servico.ativo = request.POST.get('ativo') == 'on'
        
        if request.FILES.get('imagem'):
            servico.imagem = request.FILES.get('imagem')
        
        servico.save()
        
        messages.success(request, 'Serviço atualizado com sucesso')
        return redirect('admin_servicos')
    
    context = {
        'form': {'instance': servico}
    }
    return render(request, 'admin/servico_form.html', context)


@login_required
@user_passes_test(is_admin)
@require_POST
def deletar_servico(request, id):
    """Deletar serviço"""
    servico = get_object_or_404(Servico, id=id)
    nome = servico.nome
    servico.delete()
    
    criar_notificacao(
        admin=request.user,
        tipo='sistema',
        titulo=f'Serviço Deletado',
        mensagem=f'Serviço "{nome}" foi removido do sistema',
        icone='fas fa-trash',
        cor='#dc3545'
    )
    
    messages.success(request, 'Serviço deletado com sucesso')
    return redirect('admin_servicos')

# ============================================================
# SEÇÃO 16: PAINEL ADMINISTRATIVO - PUBLICIDADES
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_publicidades(request):
    """Gestão de publicidades"""
    publicidades = Publicidade.objects.all().order_by('-criado_em')
    
    context = {
        'publicidades': publicidades,
    }
    return render(request, 'admin/admin_publicidades.html', context)


@login_required
@user_passes_test(is_admin)
def criar_publicidade(request):
    """Criar nova publicidade"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao', '')
        imagem = request.FILES.get('imagem')
        ativa = request.POST.get('ativa') == 'on'
        
        publicidade = Publicidade.objects.create(
            titulo=titulo,
            descricao=descricao,
            imagem=imagem,
            ativa=ativa
        )
        
        criar_notificacao(
            admin=request.user,
            tipo='publicidade',
            titulo=f'Nova Publicidade Criada',
            mensagem=f'Nova publicidade "{titulo}" foi adicionada',
            icone='fas fa-bullhorn',
            cor='#ff6b00'
        )
        
        messages.success(request, 'Publicidade criada com sucesso')
        return redirect('admin_publicidades')
    
    return render(request, 'admin/publicidade_form.html', {'form': {'instance': Publicidade()}})


@login_required
@user_passes_test(is_admin)
def editar_publicidade(request, id):
    """Editar publicidade"""
    publicidade = get_object_or_404(Publicidade, id=id)
    
    if request.method == 'POST':
        publicidade.titulo = request.POST.get('titulo', publicidade.titulo)
        publicidade.descricao = request.POST.get('descricao', publicidade.descricao)
        publicidade.ativa = request.POST.get('ativa') == 'on'
        
        if request.FILES.get('imagem'):
            publicidade.imagem = request.FILES.get('imagem')
        
        publicidade.save()
        
        messages.success(request, 'Publicidade atualizada com sucesso')
        return redirect('admin_publicidades')
    
    context = {
        'form': {'instance': publicidade}
    }
    return render(request, 'admin/publicidade_form.html', context)


@login_required
@user_passes_test(is_admin)
@require_POST
def remover_publicidade(request, id):
    """Remover publicidade"""
    publicidade = get_object_or_404(Publicidade, id=id)
    titulo = publicidade.titulo
    publicidade.delete()
    
    criar_notificacao(
        admin=request.user,
        tipo='sistema',
        titulo=f'Publicidade Removida',
        mensagem=f'Publicidade "{titulo}" foi removida',
        icone='fas fa-trash',
        cor='#dc3545'
    )
    
    messages.success(request, 'Publicidade removida com sucesso')
    return redirect('admin_publicidades')

# ============================================================
# SEÇÃO 17: PAINEL ADMINISTRATIVO - PERFIL
# ============================================================

@login_required
@user_passes_test(is_admin)
def perfil_admin(request):
    """Perfil do admin"""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.email = request.POST.get('email', request.user.email)
        
        password = request.POST.get('password')
        if password:
            request.user.set_password(password)
        
        request.user.save()
        
        messages.success(request, 'Perfil atualizado com sucesso')
        return redirect('admin_perfil')
    
    return render(request, 'admin/perfil_admin.html')

# ============================================================
# SEÇÃO 18: PAINEL ADMINISTRATIVO - RELATÓRIOS
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_relatorio(request):

    agendamentos = Agendamento.objects.all()


    # ==========================
    # RESUMO
    # ==========================

    agendamentos_total = agendamentos.count()

    receita_total = agendamentos.filter(
        status_pagamento='pago'
    ).aggregate(
        total=Sum('valor_pagamento')
    )['total'] or 0


    receita_pendente = agendamentos.filter(
        status_pagamento='pendente'
    ).aggregate(
        total=Sum('valor_pagamento')
    )['total'] or 0


    receita_cancelada = agendamentos.filter(
        status_confirmacao='cancelado'
    ).aggregate(
        total=Sum('valor_pagamento')
    )['total'] or 0



    ticket_medio = 0

    if agendamentos.count():

        ticket_medio = receita_total / agendamentos.count()





    # ==========================
    # GRÁFICO STATUS
    # ==========================


    dados_status = {
        "labels":[
            "Pendentes",
            "Confirmados",
            "Cancelados",
            "Não Apareceu"
        ],

        "valores":[

            agendamentos.filter(
                status_confirmacao='pendente'
            ).count(),


            agendamentos.filter(
                status_confirmacao='confirmado'
            ).count(),


            agendamentos.filter(
                status_confirmacao='cancelado'
            ).count(),


            agendamentos.filter(
                status_confirmacao='nao_apareceu'
            ).count()

        ]
    }






    # ==========================
    # RECEITA POR SERVIÇO
    # ==========================


    receita = []

    for servico in Servico.objects.all():

        valor = agendamentos.filter(
            servico=servico,
            status_pagamento='pago'
        ).aggregate(
            total=Sum('valor_pagamento')
        )['total'] or 0


        receita.append({
            "nome":servico.nome,
            "valor":float(valor)
        })



    dados_receita = {

        "labels":[
            x["nome"] for x in receita
        ],

        "valores":[
            x["valor"] for x in receita
        ]

    }








    # ==========================
    # TENDÊNCIA
    # ==========================


    tendencia_labels=[]
    tendencia_valores=[]


    for i in range(6):

        data = timezone.now().date() - timedelta(days=i*30)


        tendencia_labels.append(
            data.strftime("%m/%Y")
        )


        tendencia_valores.append(

            agendamentos.filter(
                criado_em__month=data.month
            ).count()

        )



    dados_tendencia={

        "labels":tendencia_labels[::-1],

        "valores":tendencia_valores[::-1]

    }









    # ==========================
    # COMPARECIMENTO
    # ==========================


    dados_comparecimento={

        "labels":[
            "Compareceu",
            "Não apareceu"
        ],


        "valores":[

            agendamentos.filter(
                status_confirmacao='confirmado'
            ).count(),


            agendamentos.filter(
                status_confirmacao='nao_apareceu'
            ).count()

        ]

    }









    # ==========================
    # MÉTODOS PAGAMENTO
    # ==========================


    dados_metodos={


        "labels":[
            "Presencial"
        ],


        "valores":[

            agendamentos.filter(
                metodo_pagamento='presencial'
            ).count()

        ]

    }






    # ==========================
    # DETALHES SERVIÇOS
    # ==========================


    servicos_detalhes=[]


    for servico in Servico.objects.all():


        lista = agendamentos.filter(
            servico=servico
        )


        receita_servico = lista.filter(
            status_pagamento='pago'
        ).aggregate(
            total=Sum('valor_pagamento')
        )['total'] or 0



        servicos_detalhes.append({

            "nome":servico.nome,

            "total":lista.count(),

            "confirmados":lista.filter(
                status_confirmacao='confirmado'
            ).count(),

            "cancelados":lista.filter(
                status_confirmacao='cancelado'
            ).count(),

            "receita":receita_servico,

            "ticket_medio":
                receita_servico / lista.count()
                if lista.count() else 0

        })






    context={


        "receita_total":receita_total,

        "receita_pendente":receita_pendente,

        "receita_cancelada":receita_cancelada,

        "ticket_medio":ticket_medio,


        "servicos_detalhes":servicos_detalhes,


        "dados_status":json.dumps(dados_status),

        "dados_receita":json.dumps(dados_receita),

        "dados_tendencia":json.dumps(dados_tendencia),

        "dados_comparecimento":json.dumps(dados_comparecimento),

        "dados_metodos":json.dumps(dados_metodos),

    }



    return render(
        request,
        'admin/relatorio.html',
        context
    )
@login_required
@user_passes_test(is_admin)
def exportar_relatorio(request):
    """Exportar relatório em CSV"""
    formato = request.GET.get('formato', 'csv')
    agendamentos = Agendamento.objects.filter(status_pagamento='pago').order_by('-criado_em')
    
    if formato == 'csv':
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_agendamentos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Cliente', 'Serviço', 'Data', 'Hora', 'Valor', 'Status Confirmação', 'Status Pagamento'])
        
        for agendamento in agendamentos:
            writer.writerow([
                agendamento.id,
                agendamento.nome,
                agendamento.servico.nome,
                agendamento.data,
                agendamento.hora,
                agendamento.valor_pagamento,
                agendamento.get_status_confirmacao_display(),
                agendamento.get_status_pagamento_display(),
            ])
        
        return response
    
    return redirect('admin_relatorio')

# ============================================================
# SEÇÃO 19: PASSWORD RESET (RECUPERAÇÃO DE SENHA)
# ============================================================

class PasswordResetViewCustom(PasswordResetView):
    template_name = 'auth/password_reset.html'
    email_template_name = 'auth/password_reset_email.html'
    subject_template_name = 'auth/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetDoneViewCustom(PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'

class PasswordResetCompleteViewCustom(PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'

# ============================================================
# CHATBOT IA - OFICINA MIADAS
# ============================================================

@login_required
@login_required
def api_notificacoes(request):
    """API de notificações para cliente ou administrador."""
    if is_admin(request.user):
        qs = Notificacao.objects.filter(admin=request.user)
    else:
        qs = Notificacao.objects.filter(usuario=request.user)

    qs = qs.order_by('-criada_em')[:20]
    return JsonResponse({
        'nao_lidas': qs.filter(lida=False).count(),
        'notificacoes': [
            {
                'id': n.id,
                'titulo': n.titulo,
                'mensagem': n.mensagem,
                'lida': n.lida,
                'criada_em': n.criada_em.isoformat(),
            }
            for n in qs
        ],
    })


@login_required
@user_passes_test(is_admin)
def api_emails(request):
    qs = Email.objects.order_by('-recebido_em')[:20]
    return JsonResponse({
        'nao_lidos': qs.filter(status='nao_lido').count(),
        'emails': [
            {
                'id': email.id,
                'assunto': email.assunto,
                'remetente': email.email_remetente,
                'lido': email.status != 'nao_lido',
                'criado_em': email.recebido_em.isoformat(),
            }
            for email in qs
        ],
    })


@login_required
@user_passes_test(is_admin)
@require_POST
def api_deletar_notificacao(request, id):
    notificacao = get_object_or_404(Notificacao, id=id, admin=request.user)
    notificacao.delete()
    return JsonResponse({'sucesso': True})


@login_required
@user_passes_test(is_admin)
@require_POST
def api_deletar_email(request, id):
    email = get_object_or_404(Email, id=id)
    email.delete()
    return JsonResponse({'sucesso': True})


@login_required
def chat_cliente(request):
    """Conversa entre o cliente autenticado e o administrador."""
    admin = User.objects.filter(perfil__tipo='ADM', is_active=True).order_by('id').first()
    mensagens = Mensagem.objects.none()

    if admin:
        mensagens = Mensagem.objects.filter(
            Q(remetente=request.user, destinatario=admin) |
            Q(remetente=admin, destinatario=request.user)
        ).order_by('criada_em')

        Mensagem.objects.filter(
            remetente=admin,
            destinatario=request.user,
            lida=False,
        ).update(lida=True, lida_em=timezone.now())

    return render(
        request,
        'home/chat.html',
        {'admin': admin, 'mensagens': mensagens},
    )


@login_required
@user_passes_test(is_admin)
def chat_admin(request):
    """Painel de conversas do administrador."""
    clientes_ids = Mensagem.objects.values_list(
        'remetente_id', 'destinatario_id'
    )

    ids = set()
    for remetente_id, destinatario_id in clientes_ids:
        if remetente_id != request.user.id:
            ids.add(remetente_id)
        if destinatario_id != request.user.id:
            ids.add(destinatario_id)

    clientes = User.objects.filter(
        id__in=ids,
        perfil__tipo='CLIENTE',
        is_active=True,
    ).order_by('first_name', 'username')

    cliente_id = request.GET.get('cliente')
    cliente = None
    mensagens = Mensagem.objects.none()

    if cliente_id:
        cliente = get_object_or_404(
            User,
            id=cliente_id,
            perfil__tipo='CLIENTE',
            is_active=True,
        )
        mensagens = Mensagem.objects.filter(
            Q(remetente=request.user, destinatario=cliente) |
            Q(remetente=cliente, destinatario=request.user)
        ).order_by('criada_em')

        Mensagem.objects.filter(
            remetente=cliente,
            destinatario=request.user,
            lida=False,
        ).update(lida=True, lida_em=timezone.now())

    conversas = []
    for cliente_item in clientes:
        ultima = Mensagem.objects.filter(
            Q(remetente=request.user, destinatario=cliente_item) |
            Q(remetente=cliente_item, destinatario=request.user)
        ).order_by('-criada_em').first()
        if ultima:
            conversas.append(ultima)

    conversas.sort(key=lambda mensagem: mensagem.criada_em, reverse=True)

    return render(
        request,
        'admin/chat.html',
        {
            'conversas': conversas,
            'cliente': cliente,
            'mensagens': mensagens,
        },
    )


@login_required
@require_POST
def enviar_mensagem_cliente(request):
    """Recebe uma mensagem enviada pelo cliente."""
    admin = User.objects.filter(
        perfil__tipo='ADM',
        is_active=True,
    ).order_by('id').first()

    conteudo = request.POST.get('conteudo', '').strip()
    if not admin:
        return JsonResponse(
            {'status': 'erro', 'mensagem': 'Não existe administrador disponível.'},
            status=503,
        )

    if not conteudo:
        return JsonResponse(
            {'status': 'erro', 'mensagem': 'A mensagem não pode estar vazia.'},
            status=400,
        )

    Mensagem.objects.create(
        remetente=request.user,
        destinatario=admin,
        tipo_remetente='cliente',
        conteudo=conteudo,
    )
    return JsonResponse({'status': 'sucesso'})


@login_required
@user_passes_test(is_admin)
@require_POST
def enviar_mensagem_admin(request):
    """Recebe uma mensagem enviada pelo administrador."""
    cliente_id = request.POST.get('cliente_id')
    conteudo = request.POST.get('conteudo', '').strip()

    if not cliente_id or not conteudo:
        return JsonResponse(
            {'status': 'erro', 'mensagem': 'Cliente e mensagem são obrigatórios.'},
            status=400,
        )

    cliente = get_object_or_404(
        User,
        id=cliente_id,
        perfil__tipo='CLIENTE',
        is_active=True,
    )

    Mensagem.objects.create(
        remetente=request.user,
        destinatario=cliente,
        tipo_remetente='admin',
        conteudo=conteudo,
    )
    return JsonResponse({'status': 'sucesso'})


def chatbot(request):
    return render(request, 'home/chatbot.html')

@login_required
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        msg = data.get("mensagem", "").lower()

        respostas = {
            "oi": "Olá 👋 Bem-vindo à Oficina Miadas!",
            "olá": "Olá 👋 Como posso ajudar?",
            "serviços": "Temos mecânica geral, diagnóstico, troca de óleo e travões.",
            "manutenção": "Fazemos manutenção completa para o seu veículo.",
            "agendar": "Pode agendar na área de serviços do sistema.",
            "preço": "Os preços variam conforme o serviço escolhido.",
            "horário": "Funcionamos de 08h às 17h, de segunda a sexta."
        }

        resposta = "Desculpa 🤖 ainda estou a aprender, tenta perguntar de outra forma."

        for key in respostas:
            if key in msg:
                resposta = respostas[key]
                break

        return JsonResponse({
            "resposta": resposta
        })

# ============================================================
# NOVA FUNCIONALIDADE: GERAR PDF DO AGENDAMENTO
# ============================================================

@login_required
def gerar_pdf_agendamento(request, agendamento_id):
    """Gera PDF profissional do agendamento"""

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id,
        usuario=request.user
    )


    buffer = io.BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )


    largura, altura = A4



    # =====================================================
    # CABEÇALHO
    # =====================================================

    pdf.setFillColor(colors.HexColor("#fff"))

    pdf.rect(
        0,
        altura - 120,
        largura,
        120,
        fill=1,
        stroke=0
    )


    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        50,
        altura - 55,
        "OFICINA MIADAS"
    )


    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        altura - 78,
        "Sistema de Gestão de Serviços Automotivos"
    )



    pdf.setFont(
        "Helvetica-Bold",
        12
    )


    pdf.drawRightString(
        largura - 50,
        altura - 55,
        "COMPROVATIVO"
    )


    pdf.drawRightString(
        largura - 50,
        altura - 75,
        f"Nº #{agendamento.id}"
    )





    # =====================================================
    # INFORMAÇÕES PRINCIPAIS
    # =====================================================

    y = altura - 170


    pdf.setFillColor(colors.black)


    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Dados do Cliente"
    )


    y -= 25


    pdf.setFont(
        "Helvetica",
        12
    )


    dados_cliente = [

        f"Nome: {agendamento.nome}",

        f"Email: {agendamento.email}",

        f"Telefone: {agendamento.telefone}",

    ]


    for linha in dados_cliente:

        pdf.drawString(
            60,
            y,
            linha
        )

        y -= 20





    # =====================================================
    # SERVIÇO
    # =====================================================


    y -= 20


    pdf.setFont(
        "Helvetica-Bold",
        14
    )


    pdf.drawString(
        50,
        y,
        "Detalhes do Serviço"
    )


    y -= 25


    pdf.setFont(
        "Helvetica",
        12
    )


    detalhes = [

        f"Serviço: {agendamento.servico.nome}",

        f"Data: {agendamento.data.strftime('%d/%m/%Y')}",

        f"Hora: {agendamento.hora.strftime('%H:%M')}",

        f"Valor: {agendamento.valor_pagamento} Kz",

    ]



    for linha in detalhes:


        pdf.drawString(
            60,
            y,
            linha
        )

        y -= 20






    # =====================================================
    # STATUS
    # =====================================================


    y -= 20


    pdf.setFillColor(
        colors.HexColor("#f5f5f5")
    )


    pdf.roundRect(
        50,
        y-70,
        largura-100,
        90,
        10,
        fill=1,
        stroke=0
    )


    pdf.setFillColor(colors.black)


    pdf.setFont(
        "Helvetica-Bold",
        13
    )


    pdf.drawString(
        65,
        y,
        "Estado do Agendamento"
    )



    pdf.setFont(
        "Helvetica",
        12
    )


    pdf.drawString(
        65,
        y-25,
        f"Confirmação: {agendamento.get_status_confirmacao_display()}"
    )


    pdf.drawString(
        65,
        y-45,
        f"Pagamento: {agendamento.get_status_pagamento_display()}"
    )







    # =====================================================
    # OBSERVAÇÕES
    # =====================================================


    y -= 120


    pdf.setFont(
        "Helvetica-Bold",
        13
    )


    pdf.drawString(
        50,
        y,
        "Observações"
    )


    pdf.setFont(
        "Helvetica",
        11
    )


    pdf.drawString(
        60,
        y-25,
        agendamento.observacoes or "Nenhuma observação"
    )






    # =====================================================
    # RODAPÉ
    # =====================================================


    pdf.setStrokeColor(
        colors.HexColor("#dddddd")
    )


    pdf.line(
        50,
        70,
        largura-50,
        70
    )



    pdf.setFont(
        "Helvetica-Oblique",
        9
    )


    pdf.setFillColor(
        colors.grey
    )


    pdf.drawString(
        50,
        50,
        "Documento gerado automaticamente pelo sistema Oficina Miadas"
    )


    pdf.drawRightString(
        largura-50,
        50,
        timezone.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )



    pdf.showPage()

    pdf.save()



    buffer.seek(0)



    return HttpResponse(
        buffer,
        content_type="application/pdf"
    )

# ============================================================
# OUTRAS VIEWS FALTANTES (BASEADAS NAS URLS)
# ============================================================

@login_required
def perfil(request):
    return render(request, 'home/perfil.html')

@login_required
def publicidades_view(request):
    publicidades = Publicidade.objects.filter(ativa=True)
    return render(request, 'home/publicidades.html', {'publicidades': publicidades})

@login_required
def notificacao_cliente(request):
    """Página de notificações do cliente"""

    notificacoes = Notificacao.objects.filter(
        usuario=request.user
    ).order_by('-criada_em')


    context = {
        'notificacoes': notificacoes,
    }


    return render(
        request,
        'home/notificacoes.html',
        context
    )

@login_required
def configuracoes(request):
    return render(request, 'home/configuracoes.html')

@login_required
@user_passes_test(is_admin)
def exportar_relatorio_pdf(request):

    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle
    )

    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors



    buffer = io.BytesIO()


    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )



    elementos = []


    estilos = getSampleStyleSheet()



    # ==================================================
    # TÍTULO
    # ==================================================

    titulo = ParagraphStyle(
        'titulo',
        parent=estilos['Title'],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=colors.HexColor("#ff9500")
    )


    elementos.append(
        Paragraph(
            "OFICINA MIADAS",
            titulo
        )
    )


    elementos.append(
        Paragraph(
            "Relatório Administrativo de Agendamentos",
            estilos['Heading2']
        )
    )


    elementos.append(
        Spacer(1,20)
    )




    # ==================================================
    # DADOS GERAIS
    # ==================================================


    total_agendamentos = Agendamento.objects.count()


    confirmados = Agendamento.objects.filter(
        status_confirmacao='confirmado'
    ).count()



    pendentes = Agendamento.objects.filter(
        status_confirmacao='pendente'
    ).count()



    cancelados = Agendamento.objects.filter(
        status_confirmacao='cancelado'
    ).count()



    receita_total = Agendamento.objects.filter(
        status_pagamento='pago'
    ).aggregate(
        total=Sum('valor_pagamento')
    )['total'] or 0




    receita_pendente = Agendamento.objects.filter(
        status_pagamento='pendente'
    ).aggregate(
        total=Sum('valor_pagamento')
    )['total'] or 0




    clientes = User.objects.filter(
        perfil__tipo='CLIENTE'
    ).count()




    dados = [

        ["Indicador", "Valor"],

        [
            "Total de Clientes",
            str(clientes)
        ],

        [
            "Total de Agendamentos",
            str(total_agendamentos)
        ],

        [
            "Confirmados",
            str(confirmados)
        ],

        [
            "Pendentes",
            str(pendentes)
        ],

        [
            "Cancelados",
            str(cancelados)
        ],

        [
            "Receita Total",
            f"{receita_total} Kz"
        ],

        [
            "Receita Pendente",
            f"{receita_pendente} Kz"
        ],

    ]




    tabela = Table(
        dados,
        colWidths=[250,150]
    )



    tabela.setStyle(
        TableStyle([

            (
                'BACKGROUND',
                (0,0),
                (-1,0),
                colors.HexColor("#ff9500")
            ),


            (
                'TEXTCOLOR',
                (0,0),
                (-1,0),
                colors.white
            ),


            (
                'GRID',
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),


            (
                'ALIGN',
                (1,1),
                (-1,-1),
                'CENTER'
            )

        ])
    )


    elementos.append(tabela)



    elementos.append(
        Spacer(1,30)
    )




    # ==================================================
    # SERVIÇOS
    # ==================================================


    elementos.append(
        Paragraph(
            "Desempenho por Serviço",
            estilos['Heading2']
        )
    )


    servicos = Servico.objects.all()


    dados_servicos = [

        [
            "Serviço",
            "Agendamentos",
            "Receita"
        ]

    ]



    for servico in servicos:


        quantidade = Agendamento.objects.filter(
            servico=servico
        ).count()



        receita = Agendamento.objects.filter(
            servico=servico,
            status_pagamento='pago'
        ).aggregate(
            total=Sum('valor_pagamento')
        )['total'] or 0



        dados_servicos.append(
            [
                servico.nome,
                quantidade,
                f"{receita} Kz"
            ]
        )




    tabela_servicos = Table(
        dados_servicos,
        colWidths=[200,100,100]
    )



    tabela_servicos.setStyle(
        TableStyle([

            (
                'BACKGROUND',
                (0,0),
                (-1,0),
                colors.HexColor("#333333")
            ),

            (
                'TEXTCOLOR',
                (0,0),
                (-1,0),
                colors.white
            ),


            (
                'GRID',
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            )

        ])
    )



    elementos.append(
        tabela_servicos
    )



    elementos.append(
        Spacer(1,40)
    )



    # ==================================================
    # RODAPÉ
    # ==================================================


    elementos.append(
        Paragraph(
            f"Documento gerado em {timezone.now().strftime('%d/%m/%Y %H:%M')}",
            estilos['Normal']
        )
    )


    elementos.append(
        Paragraph(
            "Sistema Web de Gestão e Divulgação - Oficina Miadas",
            estilos['Normal']
        )
    )



    pdf.build(elementos)



    buffer.seek(0)



    response = HttpResponse(
        buffer,
        content_type='application/pdf'
    )


    response['Content-Disposition'] = (
        'attachment; filename="relatorio_oficina_miadas.pdf"'
    )


    return response
    from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from .models import Agendamento


@login_required
@user_passes_test(is_admin)
def detalhes_cliente(request, cliente_id):

    cliente = get_object_or_404(User, id=cliente_id)


    agendamentos = Agendamento.objects.filter(
        usuario=cliente
    ).select_related('servico')


    dados = {

        "id": cliente.id,

        "nome": f"{cliente.first_name} {cliente.last_name}",

        "username": cliente.username,

        "email": cliente.email,

        "telefone": getattr(
            cliente.perfil,
            "telefone",
            "Não informado"
        ),

        "data_registo": cliente.date_joined.strftime(
            "%d/%m/%Y"
        ),

        "total_agendamentos": agendamentos.count(),

        "agendamentos": [

            {

                "servico": ag.servico.nome,

                "data": ag.data.strftime("%d/%m/%Y"),

                "hora": ag.hora.strftime("%H:%M"),

                "status": ag.get_status_confirmacao_display()

            }

            for ag in agendamentos

        ]

    }


    return JsonResponse(dados)




@login_required
@user_passes_test(is_admin)
def remover_cliente(request, cliente_id):

    if request.method == "POST":

        cliente = get_object_or_404(
            User,
            id=cliente_id
        )


        cliente.delete()


        return JsonResponse({

            "status": "success",

            "mensagem": "Cliente removido com sucesso"

        })


    return JsonResponse({

        "status": "error"

    }, status=400)