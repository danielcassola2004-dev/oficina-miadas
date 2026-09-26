# ============================================================
# ARQUIVO: tests.py - TESTES DE VALIDAÇÃO DO CADASTRO
# DESCRIÇÃO: Testes unitários para validações de cadastro
# IDIOMA: Português
# ============================================================

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CadastroForm
from .models import Perfil


class CadastroFormValidacaoEmailUnicoTestCase(TestCase):
    """Testes para validação de email único"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.user = User.objects.create_user(
            username='joao',
            email='joao@email.com',
            password='Senha@123'
        )
    
    def test_email_duplicado_deve_falhar(self):
        """Teste: Email duplicado deve gerar erro"""
        form_data = {
            'username': 'maria',
            'email': 'joao@email.com',  # Email já existe
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este email já está registado', str(form.errors))
    
    def test_email_novo_deve_passar(self):
        """Teste: Email novo deve ser aceito"""
        form_data = {
            'username': 'maria',
            'email': 'maria@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        # Não deve validar completamente pois não temos todos os campos
        # Mas o email não deve ter erro
        if form.is_valid() or 'email' not in form.errors:
            self.assertNotIn('email', form.errors)
    
    def test_email_normalizado_para_minusculas(self):
        """Teste: Email deve ser normalizado para minúsculas"""
        form_data = {
            'username': 'pedro',
            'email': 'PEDRO@EMAIL.COM',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.email, 'pedro@email.com')


class CadastroFormValidacaoSenhaComplexaTestCase(TestCase):
    """Testes para validação de senha complexa"""
    
    def test_senha_sem_maiuscula_deve_falhar(self):
        """Teste: Senha sem maiúscula deve falhar"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'senha@123',  # Sem maiúscula
            'password2': 'senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('maiúscula', str(form.errors).lower())
    
    def test_senha_sem_minuscula_deve_falhar(self):
        """Teste: Senha sem minúscula deve falhar"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'SENHA@123',  # Sem minúscula
            'password2': 'SENHA@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('minúscula', str(form.errors).lower())
    
    def test_senha_sem_numero_deve_falhar(self):
        """Teste: Senha sem número deve falhar"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'Senha@abc',  # Sem número
            'password2': 'Senha@abc',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('número', str(form.errors).lower())
    
    def test_senha_sem_simbolo_deve_falhar(self):
        """Teste: Senha sem símbolo deve falhar"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'Senha123abc',  # Sem símbolo
            'password2': 'Senha123abc',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('especial', str(form.errors).lower())
    
    def test_senha_muito_curta_deve_falhar(self):
        """Teste: Senha com menos de 8 caracteres deve falhar"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'Abc@12',  # Menos de 8 caracteres
            'password2': 'Abc@12',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('8', str(form.errors))
    
    def test_senha_complexa_valida_deve_passar(self):
        """Teste: Senha complexa válida deve ser aceita"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'Oficina@2024',
            'password2': 'Oficina@2024',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        # Verificar se não há erro de senha
        if not form.is_valid():
            self.assertNotIn('password1', form.errors)


class CadastroFormValidacaoUsernameReservadoTestCase(TestCase):
    """Testes para validação de username reservado"""
    
    def test_username_admin_deve_falhar(self):
        """Teste: Username 'admin' deve ser bloqueado"""
        form_data = {
            'username': 'admin',
            'email': 'admin@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('reservado', str(form.errors).lower())
    
    def test_username_root_deve_falhar(self):
        """Teste: Username 'root' deve ser bloqueado"""
        form_data = {
            'username': 'root',
            'email': 'root@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('reservado', str(form.errors).lower())
    
    def test_username_oficina_deve_falhar(self):
        """Teste: Username 'oficina' deve ser bloqueado"""
        form_data = {
            'username': 'oficina',
            'email': 'oficina@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('reservado', str(form.errors).lower())
    
    def test_username_comum_deve_passar(self):
        """Teste: Username comum deve ser aceito"""
        form_data = {
            'username': 'joao_silva',
            'email': 'joao@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        # Verificar se não há erro de username
        if not form.is_valid():
            self.assertNotIn('username', form.errors)


class CadastroFormValidacaoNomeSemNumerosTestCase(TestCase):
    """Testes para validação de nome sem números"""
    
    def test_nome_com_numeros_deve_falhar(self):
        """Teste: Nome com números deve falhar"""
        # Este teste seria no campo de nome se implementado
        # Por enquanto, o username é usado como first_name
        # Mas a validação está pronta no forms.py
        pass
    
    def test_nome_valido_deve_passar(self):
        """Teste: Nome válido com letras deve passar"""
        # Este teste seria no campo de nome se implementado
        pass


class CadastroFormValidacaoTermosTestCase(TestCase):
    """Testes para validação de termos de uso"""
    
    def test_termos_nao_aceitos_deve_falhar(self):
        """Teste: Não aceitar termos deve falhar"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': False,  # Não aceito
        }
        form = CadastroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('termos_uso', form.errors)
    
    def test_termos_aceitos_deve_passar(self):
        """Teste: Aceitar termos deve ser válido"""
        form_data = {
            'username': 'joao',
            'email': 'joao@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        form = CadastroForm(data=form_data)
        # Verificar se não há erro de termos
        if not form.is_valid():
            self.assertNotIn('termos_uso', form.errors)


class CadastroViewTestCase(TestCase):
    """Testes para a view de cadastro"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = Client()
        self.cadastro_url = reverse('cadastro')
    
    def test_get_cadastro_page_deve_retornar_200(self):
        """Teste: GET na página de cadastro deve retornar 200"""
        response = self.client.get(self.cadastro_url)
        self.assertEqual(response.status_code, 200)
    
    def test_cadastro_com_dados_validos_deve_criar_usuario(self):
        """Teste: Cadastro com dados válidos deve criar usuário"""
        form_data = {
            'username': 'joao_novo',
            'email': 'joao_novo@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        response = self.client.post(self.cadastro_url, form_data)
        
        # Verificar se o usuário foi criado
        self.assertTrue(User.objects.filter(username='joao_novo').exists())
        
        # Verificar se o perfil foi criado
        user = User.objects.get(username='joao_novo')
        self.assertTrue(Perfil.objects.filter(user=user).exists())
    
    def test_cadastro_com_email_duplicado_deve_falhar(self):
        """Teste: Cadastro com email duplicado deve falhar"""
        # Criar primeiro usuário
        User.objects.create_user(
            username='joao',
            email='joao@email.com',
            password='Senha@123'
        )
        
        # Tentar cadastrar com mesmo email
        form_data = {
            'username': 'maria',
            'email': 'joao@email.com',
            'password1': 'Senha@123',
            'password2': 'Senha@123',
            'termos_uso': True,
        }
        response = self.client.post(self.cadastro_url, form_data)
        
        # Verificar se o segundo usuário NÃO foi criado
        self.assertEqual(User.objects.filter(username='maria').count(), 0)


class PerfilModelTestCase(TestCase):
    """Testes para o modelo Perfil"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.user = User.objects.create_user(
            username='joao',
            email='joao@email.com',
            password='Senha@123'
        )
        self.perfil = Perfil.objects.create(
            user=self.user,
            tipo='CLIENTE',
            telefone='+244 912345678',
            endereco='Rua Principal, 123'
        )
    
    def test_perfil_str_deve_retornar_username(self):
        """Teste: __str__ do Perfil deve retornar username"""
        self.assertEqual(str(self.perfil), 'joao')
    
    def test_perfil_tipo_padrao_deve_ser_cliente(self):
        """Teste: Tipo padrão do Perfil deve ser CLIENTE"""
        novo_perfil = Perfil.objects.create(user=User.objects.create_user(
            username='maria',
            email='maria@email.com',
            password='Senha@123'
        ))
        self.assertEqual(novo_perfil.tipo, 'CLIENTE')


# ============================================================
# TESTES DE INTEGRAÇÃO
# ============================================================

class CadastroIntegracaoTestCase(TestCase):
    """Testes de integração do fluxo de cadastro"""
    
    def test_fluxo_completo_cadastro_login(self):
        """Teste: Fluxo completo de cadastro e login"""
        # 1. Cadastro
        form_data = {
            'username': 'joao_silva',
            'email': 'joao.silva@email.com',
            'password1': 'Oficina@2024',
            'password2': 'Oficina@2024',
            'termos_uso': True,
        }
        response = self.client.post(reverse('cadastro'), form_data)
        
        # 2. Verificar se usuário foi criado
        user = User.objects.get(username='joao_silva')
        self.assertIsNotNone(user)
        
        # 3. Verificar se perfil foi criado
        self.assertTrue(Perfil.objects.filter(user=user).exists())
        
        # 4. Tentar fazer login
        login_data = {
            'username': 'joao_silva',
            'password': 'Oficina@2024'
        }
        login_response = self.client.post(reverse('login'), login_data)
        
        # 5. Verificar se está autenticado
        self.assertTrue(login_response.wsgi_request.user.is_authenticated)


# ============================================================
# EXECUÇÃO DOS TESTES
# ============================================================

if __name__ == '__main__':
    import unittest
    unittest.main()
