from rest_framework import serializers
from .models import Funcionario, Posto

class PostoSerializer(serializers.ModelSerializer):
    # Campo calculado: conta quantos funcionários ativos existem neste posto
    total_funcionarios = serializers.SerializerMethodField()

    class Meta:
        model = Posto
        fields = ['id', 'nome', 'cidade', 'quadro_ideal', 'total_funcionarios']

    def get_total_funcionarios(self, obj):
        return obj.equipe.filter(is_active=True).count()

class FuncionarioSerializer(serializers.ModelSerializer):
    posto_nome = serializers.ReadOnlyField(source='posto_trabalho.nome')
    cargo_display = serializers.CharField(source='get_cargo_display', read_only=True)

    class Meta:
        model = Funcionario
        # Ocultamos a senha e dados sensíveis na listagem padrão
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 
                  'cargo', 'cargo_display', 'posto_trabalho', 'posto_nome', 
                  'matricula', 'telefone', 'is_active', 'data_admissao', 'data_demissao', 'foto_perfil']