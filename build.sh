#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput

if [ "$(python manage.py shell -c "from core.models import Servico; print(Servico.objects.count())" | tail -n 1)" = "0" ]; then
    python manage.py loaddata servicos.json
fi

if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model
from core.models import Perfil
import os

User = get_user_model()
username = os.environ['ADMIN_USERNAME']
email = os.environ['ADMIN_EMAIL']
password = os.environ['ADMIN_PASSWORD']

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': email,
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    }
)

if created:
    user.set_password(password)
    user.save()
else:
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.email = email
    user.set_password(password)
    user.save()

perfil, perfil_created = Perfil.objects.get_or_create(
    user=user,
    defaults={'tipo': 'ADM'}
)

if not perfil_created and perfil.tipo != 'ADM':
    perfil.tipo = 'ADM'
    perfil.save()

print('Administrador configurado com sucesso.')
"
fi

python manage.py collectstatic --noinput