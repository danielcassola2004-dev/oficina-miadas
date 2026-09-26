from django.contrib import admin
from .models import Servico, Agendamento, Perfil
from .models import Notificacao, Email

admin.site.register(Servico)
admin.site.register(Agendamento)
admin.site.register(Perfil)
admin.site.register(Notificacao)
admin.site.register(Email)
