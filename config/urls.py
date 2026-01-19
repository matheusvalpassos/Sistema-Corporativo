from django.contrib import admin
from django.urls import path, include
from core.views import home # Importe a view que acabamos de criar

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota raiz (quando acessa o site direto)
    path('', home, name='home'),

    # As rotas da API
    path('api/core/', include('core.urls')),
    #path('api/comercial/', include('comercial.urls')),
]