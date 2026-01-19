from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FuncionarioViewSet, PostoViewSet

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'postos', PostoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]