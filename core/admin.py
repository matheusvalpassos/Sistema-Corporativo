from django.contrib import admin
from .models import Funcionario, Posto, Bandeira # Importe Bandeira

admin.site.register(Funcionario)
admin.site.register(Posto)
admin.site.register(Bandeira) # Registre aqui