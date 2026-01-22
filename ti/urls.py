from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AtivoViewSet, ChamadoViewSet, AcompanhamentoViewSet

router = DefaultRouter()
router.register(r'ativos', AtivoViewSet)
router.register(r'chamados', ChamadoViewSet, basename='chamado')
router.register(r'acompanhamentos', AcompanhamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]