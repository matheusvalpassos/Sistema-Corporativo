from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# IMPORTANTE: Adicione lista_postos aqui no final 👇
from core.views import home, lista_funcionarios, lista_postos 
from ti.views import quadro_chamados
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('', home, name='home'),
    path('funcionarios/', lista_funcionarios, name='funcionarios'),
    
    # Agora vai funcionar porque importamos a função acima
    path('postos/', lista_postos, name='postos'),
    
    path('ti/chamados/', quadro_chamados, name='ti_chamados'),

    path('api/core/', include('core.urls')),
    path('api/ti/', include('ti.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)