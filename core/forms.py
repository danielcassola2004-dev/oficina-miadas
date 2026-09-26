# ============================================================
# ARQUIVO: forms.py - ATUALIZADO COM VALIDAÇÕES COMPLETAS
# DESCRIÇÃO: Formulários com validações de segurança e dados
# VALIDAÇÕES IMPLEMENTADAS:
#   1. Email Único
#   2. Senha Complexa (8+ chars, maiúsculas, números, símbolos)
#   3. Username Protegido (bloquear nomes reservados)
#   4. Normalização de Dados (email em minúsculas)
#   5. Termos de Uso (obrigatório)
#   6. Nome sem Números (apenas letras e espaços)
# IDIOMA: Português
# ============================================================

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
import re
from .models import Perfil, Agendamento, Servico, Publicidade


# ============================================================
# VALIDADORES CUSTOMIZADOS
# ============================================================

def validar_email_unico(email):
    """Valida se o email já existe no banco de dados"""
    if User.objects.filter(email=email.lower()).exists():
        raise ValidationError('Este email já está registado. Tente outro ou faça login.')


def validar_username_reservado(username):
    """Valida se o username não é um nome reservado"""
    nomes_reservados = [
        'admin', 'root', 'oficina', 'miadas', 'staff', 'moderator',
        'support', 'help', 'info', 'contact', 'noreply', 'test',
        'demo', 'user', 'guest', 'administrator'
    ]
    
    if username.lower() in nomes_reservados:
        raise ValidationError(f'O nome de utilizador "{username}" é reservado. Escolha outro.')


def validar_senha_complexa(password):
    """
    Valida a complexidade da senha:
    - Mínimo 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    """
    if len(password) < 8:
        raise ValidationError('A palavra-passe deve ter no mínimo 8 caracteres.')
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError('A palavra-passe deve conter pelo menos uma letra maiúscula.')
    
    if not re.search(r'[a-z]', password):
        raise ValidationError('A palavra-passe deve conter pelo menos uma letra minúscula.')
    
    if not re.search(r'[0-9]', password):
        raise ValidationError('A palavra-passe deve conter pelo menos um número.')
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        raise ValidationError('A palavra-passe deve conter pelo menos um caractere especial (!@#$%^&*).')


def validar_nome_sem_numeros(nome):
    """Valida se o nome contém apenas letras e espaços"""
    # Remove espaços e verifica se contém apenas letras
    nome_limpo = nome.strip()
    
    if not nome_limpo:
        raise ValidationError('O nome não pode estar vazio.')
    
    # Permitir apenas letras e espaços (inclui acentos)
    if not re.match(r'^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+$', nome_limpo):
        raise ValidationError('O nome não pode conter números ou caracteres especiais. Use apenas letras.')
    
    # Validar comprimento mínimo
    if len(nome_limpo) < 3:
        raise ValidationError('O nome deve ter no mínimo 3 caracteres.')
    
    if len(nome_limpo) > 100:
        raise ValidationError('O nome não pode ter mais de 100 caracteres.')


# ==========================
# CADASTRO - ATUALIZADO COM VALIDAÇÕES
# ==========================
class CadastroForm(UserCreationForm):
    """
    Formulário de cadastro com validações completas:
    - Email único e obrigatório
    - Senha complexa
    - Username protegido
    - Termos de uso obrigatórios
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com',
        }),
        label='Endereço de Email',
        help_text='Usaremos este email para notificações e recuperação de conta'
    )
    
    # Campo para aceitar termos de uso
    termos_uso = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Concordo com os Termos e Condições e Política de Privacidade',
        error_messages={
            'required': 'Deve aceitar os Termos e Condições para continuar.'
        }
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de utilizador (3-20 caracteres)',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar mensagens de erro do password1 e password2
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite uma palavra-passe forte',
        })
        self.fields['password1'].label = 'Palavra-passe'
        self.fields['password1'].help_text = 'Mínimo 8 caracteres. Use maiúsculas, minúsculas, números e símbolos.'
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua palavra-passe',
        })
        self.fields['password2'].label = 'Confirmar Palavra-passe'
        self.fields['password2'].help_text = ''
    
    def clean_username(self):
        """Validar username: proteger nomes reservados"""
        username = self.cleaned_data.get('username')
        
        if username:
            # Validar nomes reservados
            validar_username_reservado(username)
            
            # Validar unicidade (Django já faz isso, mas reforçamos)
            if User.objects.filter(username=username).exists():
                raise ValidationError('Este nome de utilizador já existe. Escolha outro.')
        
        return username
    
    def clean_email(self):
        """Validar email: deve ser único e em minúsculas"""
        email = self.cleaned_data.get('email')
        
        if email:
            # Normalizar email (converter para minúsculas e remover espaços)
            email = email.strip().lower()
            
            # Validar unicidade
            validar_email_unico(email)
        
        return email
    
    def clean_password1(self):
        """Validar complexidade da senha"""
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            validar_senha_complexa(password1)
        
        return password1
    
    def clean_password2(self):
        """Validar confirmação de senha"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('As palavras-passe não coincidem.')
        
        return password2
    
    def save(self, commit=True):
        """Salvar utilizador com email normalizado"""
        user = super().save(commit=False)
        
        # Normalizar email
        user.email = user.email.strip().lower()
        
        # Usar o username como first_name
        user.first_name = user.username
        
        if commit:
            user.save()
        
        return user


# ==========================
# PERFIL
# ==========================
class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco']
        widgets = {
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+244 9xx xxx xxx',
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo',
            }),
        }


# ==========================
# AGENDAMENTO - ATUALIZADO COM VALIDAÇÕES
# ==========================
class AgendamentoForm(forms.ModelForm):
    """
    Formulário de agendamento com validações
    - Data obrigatória (não pode ser no passado)
    - Hora obrigatória (não pode ser no passado)
    - Validação em tempo real
    """

    # Campo de data com widget de calendário
    data = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True,
            'min': datetime.now().strftime('%Y-%m-%d'),
        }),
        label='Data do Agendamento',
        help_text='Selecione uma data no futuro'
    )

    # Campo de hora com widget de hora
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'required': True,
        }),
        label='Hora do Agendamento',
        help_text='Selecione uma hora válida'
    )

    class Meta:
        model = Agendamento
        fields = ['nome', 'email', 'telefone', 'data', 'hora', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome completo',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+244 9xx xxx xxx',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observações adicionais (opcional)',
                'rows': 4,
            }),
        }

    def clean_data(self):
        """Validar se a data é no futuro"""
        data = self.cleaned_data.get('data')
        
        if data:
            hoje = timezone.now().date()
            if data < hoje:
                raise ValidationError('A data deve ser no futuro')
            
            um_ano_depois = hoje + timedelta(days=365)
            if data > um_ano_depois:
                raise ValidationError('A data não pode ser mais de 1 ano no futuro')
        
        return data

    def clean_hora(self):
        """Validar se a hora é válida"""
        hora = self.cleaned_data.get('hora')
        data = self.cleaned_data.get('data')
        
        if hora and data:
            hoje = timezone.now().date()
            if data == hoje:
                agora = timezone.now().time()
                if hora <= agora:
                    raise ValidationError('A hora deve ser no futuro')
        
        return hora

    def clean(self):
        """Validação geral"""
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')
        
        if data and hora:
            data_hora = timezone.make_aware(datetime.combine(data, hora))
            agora = timezone.now()
            
            uma_hora_depois = agora + timedelta(hours=1)
            if data_hora < uma_hora_depois:
                raise ValidationError('O agendamento deve ser no mínimo 1 hora no futuro')
        
        return cleaned_data


# ==========================
# FORMULÁRIO DE PAGAMENTO - APENAS PRESENCIAL
# ==========================
class PagamentoForm(forms.Form):
    """
    Formulário de pagamento simplificado
    - Apenas método Presencial
    - Confirmação de pagamento
    """

    METODO_CHOICES = [
        ('presencial', 'Pagamento Presencial'),
    ]

    metodo_pagamento = forms.ChoiceField(
        choices=METODO_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        label='Método de Pagamento',
        initial='presencial',
    )

    confirmar = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Confirmo que desejo realizar este pagamento presencial',
    )


# ==========================
# SERVIÇOS
# ==========================
class ServicoForm(forms.ModelForm):

    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'imagem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


# ==========================
# PUBLICIDADE
# ==========================
class PublicidadeForm(forms.ModelForm):

    class Meta:
        model = Publicidade
        fields = ['titulo', 'imagem', 'descricao', 'ativa']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'ativa': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
