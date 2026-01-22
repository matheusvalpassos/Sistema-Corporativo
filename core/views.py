from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum
from .models import Funcionario, Posto, Bandeira
from .serializers import FuncionarioSerializer, PostoSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class PostoViewSet(viewsets.ModelViewSet):
    queryset = Posto.objects.all()
    serializer_class = PostoSerializer
    permission_classes = [IsAuthenticated]

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]

    # Rota personalizada para devolver dados do Dashboard
    # URL final: /api/core/funcionarios/dashboard_metrics/
    @action(detail=False, methods=['get'])
    def dashboard_metrics(self, request):
        total_ativos = Funcionario.objects.filter(is_active=True).count()
        total_postos = Posto.objects.count()
        
        # Agrupamento: Quantos funcionários por cargo?
        # Ex: [{'cargo': 'FRENT', 'total': 15}, {'cargo': 'GER_POSTO', 'total': 3}]
        por_cargo = Funcionario.objects.filter(is_active=True).values('cargo').annotate(total=Count('id'))
        
        # Custo Mensal Estimado (Soma dos salários)
        custo_folha = Funcionario.objects.filter(is_active=True).aggregate(Sum('salario_base'))['salario_base__sum'] or 0

        return Response({
            "cards": {
                "total_funcionarios": total_ativos,
                "total_postos": total_postos,
                "folha_estimada": custo_folha
            },
            "graficos": {
                "distribuicao_cargos": por_cargo
            }
        })
        
# Essa função apenas "pinta" o HTML na tela
@login_required(login_url='/admin/login/') # Se não estiver logado, manda pro login do Admin por enquanto
def home(request):
    return render(request, 'index.html')

# Chamamos essa função quando acessamos /funcionarios/ pro HTML renderizar as funções
@login_required(login_url='/admin/login/')
def lista_funcionarios(request):
    # Passamos as tuplas de opções e a lista de postos reais para o HTML
    context = {
        'opcoes_setores': Funcionario.SETORES,
        'opcoes_cargos': Funcionario.CARGOS,
        'lista_postos': Posto.objects.all(), # Para preencher o select de postos
    }
    return render(request, 'funcionarios.html', context)

@login_required(login_url='login')
def lista_postos(request):
    # Busca todas as bandeiras cadastradas para o select
    opcoes_bandeiras = Bandeira.objects.all()
    return render(request, 'postos.html', {'opcoes_bandeiras': opcoes_bandeiras})

@login_required
def perfil_usuario(request):
    return render(request, 'perfil.html')

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html') # <--- Cai aqui se não tiver logado
    return render(request, 'index.html') # <--- Cai aqui se tiver logado