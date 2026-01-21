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
        # Define automaticamente o solicitante como o usuário logado
        serializer.save(solicitante=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # Se for do setor TI ou CEO, vê tudo
        if user.setor == 'TI' or user.cargo == 'CEO':
            return Chamado.objects.all().order_by('-criado_em')
        
        # Se for gerente de posto, vê só os do posto dele
        if user.posto_trabalho:
            return Chamado.objects.filter(posto=user.posto_trabalho).order_by('-criado_em')
        
        # Padrão: vê só os que ele mesmo abriu
        return Chamado.objects.filter(solicitante=user).order_by('-criado_em')

    # Rota para Dashboard de TI
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        # Totais gerais
        total_abertos = Chamado.objects.exclude(status__in=['RESOLVIDO', 'FECHADO']).count()
        ativos_manutencao = Ativo.objects.filter(status='MANUT').count()
        
        # Chamados por Prioridade (ex: Alta: 5, Média: 2)
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
    
    # ADICIONE ISSO AQUI 👇
    def perform_create(self, serializer):
        # Grava quem está enviando a mensagem (Técnico ou Usuário Comum)
        serializer.save(autor=self.request.user)

class CategoriaAtivoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaAtivo.objects.all()
    serializer_class = CategoriaAtivoSerializer
    permission_classes = [IsAuthenticated]



# View para renderizar o HTML (Frontend)
@login_required(login_url='login')
def quadro_chamados(request):
    return render(request, 'ti/chamados.html')