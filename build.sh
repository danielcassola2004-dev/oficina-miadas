#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput

if [ "$(python manage.py shell -c "from core.models import Servico; print(Servico.objects.count())" | tail -n 1)" = "0" ]; then
    python manage.py loaddata servicos.json
fi

python manage.py collectstatic --noinput