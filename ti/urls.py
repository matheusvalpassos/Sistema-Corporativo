from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AtivoViewSet, ChamadoViewSet, AcompanhamentoViewSet, CategoriaAtivoViewSet

router = DefaultRouter()
router.register(r'ativos', AtivoViewSet)
router.register(r'chamados', ChamadoViewSet, basename='chamado')
router.register(r'acompanhamentos', AcompanhamentoViewSet)
router.register(r'categorias', CategoriaAtivoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]