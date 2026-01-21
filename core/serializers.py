from rest_framework import serializers
from .models import Funcionario, Posto, Bandeira

class PostoSerializer(serializers.ModelSerializer):
    # Campo calculado: conta quantos funcionários ativos existem neste posto
    total_funcionarios = serializers.SerializerMethodField()
    
    # Campo extra de leitura: Pega o nome da bandeira (ex: "Shell") através da relação
    # O 'source' navega pelo relacionamento: objeto.bandeira.nome
    bandeira_nome = serializers.ReadOnlyField(source='bandeira.nome')

    class Meta:
        model = Posto
        # Agora incluímos todos os campos novos + os campos extras
        fields = [
            'id', 
            'nome', 
            'cnpj', 
            'cidade', 
            'endereco', 
            'bandeira',      # ID da bandeira (para o cadastro/update)
            'bandeira_nome', # Nome da bandeira (apenas leitura para o card)
            'quadro_ideal', 
            'total_funcionarios'
        ]

    def get_total_funcionarios(self, obj):
        # Retorna 0 se não tiver equipe, ou a contagem se tiver
        return obj.equipe.filter(is_active=True).count()

class FuncionarioSerializer(serializers.ModelSerializer):
    posto_nome = serializers.ReadOnlyField(source='posto_trabalho.nome')
    cargo_display = serializers.CharField(source='get_cargo_display', read_only=True)

    class Meta:
        model = Funcionario
        # Ocultamos a senha e dados sensíveis na listagem padrão
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'cargo', 'cargo_display', 'posto_trabalho', 'posto_nome', 
            'matricula', 'telefone', 'is_active', 'data_admissao', 
            'data_demissao', 'foto_perfil'
        ]