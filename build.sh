#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput

if [ "$(python manage.py shell -c "from core.models import Servico; print(Servico.objects.count())" | tail -n 1)" = "0" ]; then
    python manage.py loaddata servicos.json
fi

if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model
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
    print('Administrador criado com sucesso.')
else:
    changed = False

    if not user.is_staff:
        user.is_staff = True
        changed = True

    if not user.is_superuser:
        user.is_superuser = True
        changed = True

    if not user.is_active:
        user.is_active = True
        changed = True

    if changed:
        user.save()
        print('Administrador existente atualizado.')
    else:
        print('Administrador já existe.')
"
fi

python manage.py collectstatic --noinput