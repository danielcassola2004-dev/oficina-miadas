from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Perfil(models.Model):

    TIPO_USUARIO = (
        ('ADM', 'Administrador'),
        ('CLIENTE', 'Cliente'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO, default='CLIENTE')

    def __str__(self):
        return self.user.username


class Servico(models.Model):

    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to='servicos/', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


# ============================================================
# MODELO ATUALIZADO: AGENDAMENTO
# DESCRIÇÃO: Dois status independentes - Confirmação e Pagamento
# STATUS CONFIRMAÇÃO: Pendente, Confirmado, Cancelado, Não Apareceu
# STATUS PAGAMENTO: Pendente, Pago
# MÉTODO PAGAMENTO: Apenas Presencial
# IDIOMA: Português
# ============================================================

class Agendamento(models.Model):

    # Comentário: Status de Confirmação (fluxo do agendamento)
    STATUS_CONFIRMACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('nao_apareceu', 'Não Apareceu'),
    ]

    # Comentário: Status de Pagamento (fluxo do pagamento)
    STATUS_PAGAMENTO_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
    ]

    # Comentário: Método de Pagamento - APENAS PRESENCIAL
    METODO_PAGAMENTO_CHOICES = [
        ('presencial', 'Pagamento Presencial'),
    ]

    # Comentário: Relacionamentos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    # Comentário: Dados do cliente
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    # Comentário: Data e hora do agendamento
    data = models.DateField()
    hora = models.TimeField()

    # Comentário: Observações adicionais
    observacoes = models.TextField(blank=True)

    # Comentário: STATUS DE CONFIRMAÇÃO (NOVO SISTEMA)
    status_confirmacao = models.CharField(
        max_length=20,
        choices=STATUS_CONFIRMACAO_CHOICES,
        default='pendente',
        verbose_name='Status de Confirmação'
    )
    
    # Comentário: STATUS DE PAGAMENTO (NOVO SISTEMA)
    status_pagamento = models.CharField(
        max_length=20,
        choices=STATUS_PAGAMENTO_CHOICES,
        default='pendente',
        verbose_name='Status de Pagamento'
    )

    # Comentário: Dados de pagamento
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=METODO_PAGAMENTO_CHOICES,
        default='presencial',
        verbose_name='Método de Pagamento'
    )
    valor_pagamento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_pagamento = models.DateTimeField(null=True, blank=True)
    referencia_pagamento = models.CharField(max_length=100, blank=True)

    # Comentário: Timestamps para rastreamento
    criado_em = models.DateTimeField(default=timezone.now)
    confirmado_em = models.DateTimeField(null=True, blank=True)
    cancelado_em = models.DateTimeField(null=True, blank=True)
    pago_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"{self.nome} - {self.servico.nome}"

    # ============================================================
    # MÉTODOS PARA GERENCIAR STATUS DE CONFIRMAÇÃO
    # ============================================================

    def confirmar(self):
        """Confirma o agendamento (Pendente → Confirmado)"""
        if self.status_confirmacao == 'pendente':
            self.status_confirmacao = 'confirmado'
            self.confirmado_em = timezone.now()
            self.save()
            return True
        return False

    def cancelar(self):
        """Cancela o agendamento (Confirmado → Cancelado)"""
        if self.status_confirmacao in ['pendente', 'confirmado']:
            self.status_confirmacao = 'cancelado'
            self.cancelado_em = timezone.now()
            self.save()
            return True
        return False

    def marcar_nao_apareceu(self):
        """Marca como não apareceu (Confirmado → Não Apareceu)"""
        if self.status_confirmacao == 'confirmado':
            self.status_confirmacao = 'nao_apareceu'
            self.cancelado_em = timezone.now()
            self.save()
            return True
        return False

    # ============================================================
    # MÉTODOS PARA GERENCIAR STATUS DE PAGAMENTO
    # ============================================================

    def marcar_pago(self):
        """Marca o pagamento como pago (Pendente → Pago)"""
        if self.status_pagamento == 'pendente':
            self.status_pagamento = 'pago'
            self.pago_em = timezone.now()
            self.save()
            return True
        return False

    # ============================================================
    # MÉTODOS AUXILIARES
    # ============================================================

    def pode_confirmar(self):
        """Verifica se pode ser confirmado"""
        return self.status_confirmacao == 'pendente'

    def pode_cancelar(self):
        """Verifica se pode ser cancelado"""
        return self.status_confirmacao in ['pendente', 'confirmado']

    def pode_marcar_nao_apareceu(self):
        """Verifica se pode ser marcado como não apareceu"""
        return self.status_confirmacao == 'confirmado'

    def pode_marcar_pago(self):
        """Verifica se pode ser marcado como pago"""
        return self.status_pagamento == 'pendente'


class Publicidade(models.Model):

    titulo = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='publicidades/', null=True, blank=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# ============ NOVOS MODELOS ============

class Notificacao(models.Model):
    """Modelo para armazenar notificações do admin"""

    TIPO_CHOICES = [
        ('agendamento', 'Novo Agendamento'),
        ('cliente', 'Novo Cliente'),
        ('servico', 'Novo Serviço'),
        ('publicidade', 'Nova Publicidade'),
        ('confirmacao', 'Confirmação de Agendamento'),
        ('cancelamento', 'Cancelamento de Agendamento'),
        ('pagamento', 'Pagamento Recebido'),
        ('sistema', 'Mensagem do Sistema'),
    ]

    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    icone = models.CharField(max_length=50, default='fas fa-bell')
    cor = models.CharField(max_length=50, default='#007bff')
    
    # Referência opcional para o objeto relacionado
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notificacoes_usuario')
    
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criada_em']
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f"{self.titulo} - {self.admin.username}"


class Email(models.Model):
    """Modelo para armazenar emails/mensagens de clientes"""

    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    STATUS_CHOICES = [
        ('nao_lido', 'Não Lido'),
        ('lido', 'Lido'),
        ('respondido', 'Respondido'),
        ('arquivado', 'Arquivado'),
    ]

    de = models.CharField(max_length=200)
    email_remetente = models.EmailField()
    assunto = models.CharField(max_length=300)
    mensagem = models.TextField()
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_lido')
    
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, null=True, blank=True, related_name='emails')
    
    recebido_em = models.DateTimeField(auto_now_add=True)
    respondido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-recebido_em']

    def __str__(self):
        return f"{self.assunto} - {self.de}"


# ============================================================
# MODELO: MENSAGEM (CHAT ENTRE ADMIN E CLIENTE)
# ============================================================

class Mensagem(models.Model):
    """Modelo para armazenar mensagens entre admin e cliente"""
    
    TIPO_REMETENTE = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    ]
    
    # Remetente e destinatário
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    tipo_remetente = models.CharField(max_length=10, choices=TIPO_REMETENTE)
    
    # Conteúdo
    assunto = models.CharField(max_length=200, blank=True)
    conteudo = models.TextField()
    
    # Status
    lida = models.BooleanField(default=False)
    respondida = models.BooleanField(default=False)
    
    # Timestamps
    criada_em = models.DateTimeField(auto_now_add=True)
    lida_em = models.DateTimeField(null=True, blank=True)
    
    # Relacionamento com agendamento (opcional)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, null=True, blank=True, related_name='mensagens')
    
    class Meta:
        ordering = ['-criada_em']
        verbose_name_plural = 'Mensagens'
    
    def __str__(self):
        return f"Mensagem de {self.remetente.username} para {self.destinatario.username}"
    
    def marcar_como_lida(self):
        """Marca a mensagem como lida"""
        if not self.lida:
            self.lida = True
            self.lida_em = timezone.now()
            self.save()
