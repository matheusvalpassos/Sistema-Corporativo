from django.db import models
from django.conf import settings # Para pegar o modelo de Usuário
from core.models import Posto

class CategoriaAtivo(models.Model):
    """Ex: Computador, Impressora Térmica, PinPad, Nobreak, Monitor"""
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Ativo(models.Model):
    STATUS_CHOICES = (
        ('USO', 'Em Uso'),
        ('ESTOQUE', 'Em Estoque (Reserva)'),
        ('MANUT', 'Em Manutenção'),
        ('BAIXA', 'Baixado/Descartado'),
    )

    nome = models.CharField(max_length=100) # Ex: PC Caixa 01
    patrimonio = models.CharField(max_length=50, unique=True) # Etiqueta da empresa
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.ForeignKey(CategoriaAtivo, on_delete=models.PROTECT)
    
    # Onde este equipamento está?
    posto_atual = models.ForeignKey(Posto, on_delete=models.SET_NULL, null=True, related_name='ativos_ti')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='USO')
    
    # Dados técnicos úteis para suporte remoto
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    anydesk_id = models.CharField(max_length=50, blank=True, null=True)
    
    data_compra = models.DateField(blank=True, null=True)
    garantia_ate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.patrimonio} - {self.nome} ({self.posto_atual})"

class Chamado(models.Model):
    PRIORIDADE = (
        ('1', 'Baixa - Dúvida/Solicitação'),
        ('2', 'Média - Falha Parcial'),
        ('3', 'Alta - Posto Parado/Vendas Impactadas'),
    )
    STATUS = (
        ('NOVO', 'Novo'),
        ('ANDAMENTO', 'Em Atendimento'),
        ('AGUARDANDO', 'Aguardando Usuário/Terceiro'),
        ('RESOLVIDO', 'Resolvido'),
        ('FECHADO', 'Fechado'),
    )

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    
    # Quem pediu? (Geralmente gerente do posto)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chamados_abertos')
    
    # Quem vai resolver? (Técnico de TI)
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='chamados_tecnicos')
    
    # O problema é em qual equipamento? (Opcional, pois pode ser internet)
    ativo_relacionado = models.ForeignKey(Ativo, on_delete=models.SET_NULL, null=True, blank=True)
    posto = models.ForeignKey(Posto, on_delete=models.CASCADE) # Para facilitar filtros
    
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE, default='2')
    status = models.CharField(max_length=10, choices=STATUS, default='NOVO')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    fechado_em = models.DateTimeField(null=True, blank=True)

    arquivo = models.FileField(upload_to='chamados_anexos/', null=True, blank=True)

    def __str__(self):
        return f"#{self.id} - {self.titulo}"

class Acompanhamento(models.Model):
    """Respostas e interações no ticket (Chat)"""
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='acompanhamentos')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    anexo = models.FileField(upload_to='chamados_anexos/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    # Se essa mensagem é interna (só TI vê) ou pública (usuário vê)
    is_interno = models.BooleanField(default=False)