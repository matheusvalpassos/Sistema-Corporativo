from rest_framework import serializers
from .models import Funcionario, Posto, Bandeira

class PostoSerializer(serializers.ModelSerializer):
    total_funcionarios = serializers.SerializerMethodField()
    
    bandeira_nome = serializers.ReadOnlyField(source='bandeira.nome')

    class Meta:
        model = Posto
        fields = ['id', 'nome', 'cnpj', 'cidade', 'endereco', 
            'bandeira', 'bandeira_nome', 'quadro_ideal', 'total_funcionarios']

    def get_total_funcionarios(self, obj):
        return obj.equipe.filter(is_active=True).count()

class FuncionarioSerializer(serializers.ModelSerializer):
    posto_nome = serializers.ReadOnlyField(source='posto_trabalho.nome')
    cargo_display = serializers.CharField(source='get_cargo_display', read_only=True)
    setor_display = serializers.CharField(source='get_setor_display', read_only=True)

    class Meta:
        model = Funcionario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'cargo', 'cargo_display', 'setor', 'setor_display',
            'posto_trabalho', 'posto_nome', 'matricula', 'cpf',
            'telefone', 'is_active', 'data_admissao', 'data_demissao', 'foto_perfil'
        ]
        
class BandeiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bandeira
        fields = '__all__'