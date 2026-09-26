# Oficina Miadas

Sistema Web de Gestão e Divulgação para a Oficina Miadas, desenvolvido com Django.

## Principais funcionalidades

- Cadastro e autenticação de clientes
- Área do cliente
- Gestão de serviços
- Agendamento de serviços
- Confirmação e cancelamento de agendamentos
- Pagamento presencial
- Gestão de publicidades
- Notificações
- Chat entre cliente e administração
- Chatbot
- Relatórios e exportação em PDF
- Recuperação de palavra-passe

## Desenvolvimento local

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Produção

Configure as variáveis de ambiente presentes em `.env.example`, especialmente:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- credenciais de email

Depois execute:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn oficina_miadas.wsgi:application
```

O `build.sh` já contém os comandos de migração e recolha dos ficheiros estáticos.

## Nota sobre ficheiros enviados

As imagens existentes em `media/` fazem parte da versão atual do site. Em produção, novos uploads devem ser armazenados num serviço de armazenamento persistente, pois o sistema de ficheiros de algumas hospedagens gratuitas pode ser efémero.
