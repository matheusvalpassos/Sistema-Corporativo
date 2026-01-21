import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class Bandeira(models.Model):
    nome = models.CharField(max_length=50) # Ex: Shell, Ipiranga
    
    def __str__(self):
        return self.nome

class Posto(models.Model):
    nome = models.CharField(max_length=100) # Ex: "Posto Centro", "Posto Rodovia"
    cnpj = models.CharField(max_length=18, unique=True)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    bandeira = models.ForeignKey(Bandeira, on_delete=models.PROTECT, related_name='postos')
    # Outros dados como endereço, bandeira, etc.
    
    quadro_ideal = models.IntegerField(default=10, help_text="Quantidade ideal de funcionários")

    def __str__(self):
        return self.nome


class Funcionario(AbstractUser):
    # Setores (Horizontal)
    SETORES = (
        ('DIR', 'Diretoria/CEO'),
        ('COM', 'Comercial'),
        ('TI',  'Tecnologia da Informação'),
        ('RH',  'Recursos Humanos'),
        ('MKT', 'Marketing'),
        ('ADM', 'Administrativo'),
        ('OPE', 'Operacional de Pista'), # Para frentistas
    )

    # Cargos (Vertical - Define o nível de poder)
    CARGOS = (
        ('CEO', 'CEO'),
        ('GER_SETOR', 'Gerente de Setor (Matriz)'), # Gerente TI, RH, Comercial Geral
        ('GER_POSTO', 'Gerente de Posto'),
        ('SUB_GER',   'Subgerente'),
        ('ESPEC',     'Especialista/Técnico'),
        ('ASSIST',    'Assistente/Auxiliar'),
        ('FRENT',     'Frentista'),
    )

    setor = models.CharField(max_length=3, choices=SETORES, default='OPE')
    cargo = models.CharField(max_length=10, choices=CARGOS, default='FRENT')
    
    # O Pulo do Gato: Vínculo com a Unidade
    # Se for Null, significa que é da MATRIZ (Vê tudo ou não tem posto fixo)
    posto_trabalho = models.ForeignKey(Posto, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipe')
    
    # Dados para Gestão/RH
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_admissao = models.DateField(null=True, blank=True)
    data_demissao = models.DateField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)

    # SOBRESCREVER O MÉTODO SAVE PARA GERAR MATRÍCULA
    def save(self, *args, **kwargs):
        if not self.matricula:
            # Gera um Hexadecimal de 8 dígitos (Ex: A1B2C3D4)
            # uuid4 gera algo longo, pegamos os primeiros 8 caracteres e deixamos maiúsculo
            self.matricula = uuid.uuid4().hex[:8].upper()
            
            # (Opcional) Segurança extra: Garantir que é único num loop
            while Funcionario.objects.filter(matricula=self.matricula).exists():
                self.matricula = uuid.uuid4().hex[:8].upper()
                
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_cargo_display()})"
    
    # Helper para saber se é "Chefe"
    @property
    def is_decision_maker(self):
        return self.cargo in ['CEO', 'GER_SETOR', 'GER_POSTO']