from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from .models import Ativo, Chamado, Acompanhamento, CategoriaAtivo
from .serializers import AtivoSerializer, ChamadoSerializer, AcompanhamentoSerializer, CategoriaAtivoSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class AtivoViewSet(viewsets.ModelViewSet):
    queryset = Ativo.objects.all()
    serializer_class = AtivoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['posto_atual', 'categoria', 'status']

class ChamadoViewSet(viewsets.ModelViewSet):
    serializer_class = ChamadoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'prioridade', 'posto']

    def perform_create(self, serializer):
        serializer.save(solicitante=self.request.user)

    def get_queryset(self):
        user = self.request.user
        
        # 1. VISÃO TOTAL (Superusuário, TI ou CEO): Vê todos os chamados
        if user.is_superuser or getattr(user, 'setor', '') == 'TI' or getattr(user, 'cargo', '') == 'CEO':
            return Chamado.objects.all().order_by('-criado_em')
        
        # 2. VISÃO GERENCIAL (Opcional: Gerente vê todos os chamados da sua unidade):
        # Se for gerente, vê tudo do posto. Se for funcionário comum, vê só os dele.
        if user.posto_trabalho and getattr(user, 'cargo', '') in ['GER_POSTO', 'GER_SETOR']:
            return Chamado.objects.filter(posto=user.posto_trabalho).order_by('-criado_em')
        
        return Chamado.objects.filter(solicitante=user).order_by('-criado_em')


    @action(detail=False, methods=['get'])
    def dashboard(self, request):

        total_abertos = Chamado.objects.exclude(status__in=['RESOLVIDO', 'FECHADO']).count()
        ativos_manutencao = Ativo.objects.filter(status='MANUT').count()
        por_prioridade = Chamado.objects.exclude(status='FECHADO').values('prioridade').annotate(total=Count('id'))
        
        return Response({
            "cards": {
                "chamados_abertos": total_abertos,
                "ativos_manutencao": ativos_manutencao
            },
            "graficos": {
                "prioridade": por_prioridade
            }
        })

class AcompanhamentoViewSet(viewsets.ModelViewSet):
    queryset = Acompanhamento.objects.all()
    serializer_class = AcompanhamentoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['chamado']
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class CategoriaAtivoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaAtivo.objects.all()
    serializer_class = CategoriaAtivoSerializer
    permission_classes = [IsAuthenticated]



# View para renderizar o HTML (Frontend)
@login_required(login_url='login')
def quadro_chamados(request):
    return render(request, 'ti/chamados.html')

# View para renderizar o HTML dos Ativos
@login_required(login_url='login')
def inventario_ativos(request):
    return render(request, 'ti/ativos.html')