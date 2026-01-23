from rest_framework import serializers
from .models import Ativo, Chamado, Acompanhamento, CategoriaAtivo

class CategoriaAtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaAtivo
        fields = '__all__'

class AtivoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.ReadOnlyField(source='categoria.nome')
    posto_nome = serializers.ReadOnlyField(source='posto_atual.nome')

    class Meta:
        model = Ativo
        fields = '__all__'

class AcompanhamentoSerializer(serializers.ModelSerializer):
    autor_nome = serializers.ReadOnlyField(source='autor.first_name')
    
    class Meta:
        model = Acompanhamento
        fields = ['id', 'chamado', 'autor', 'autor_nome', 'texto', 'criado_em']
        read_only_fields = ['autor', 'criado_em']

class ChamadoSerializer(serializers.ModelSerializer):
    solicitante_nome = serializers.ReadOnlyField(source='solicitante.first_name')
    posto_nome = serializers.ReadOnlyField(source='posto.nome')
    tecnico_nome = serializers.ReadOnlyField(source='tecnico.first_name')
    tecnico_foto = serializers.SerializerMethodField()
    
    # Traz as últimas interações junto (opcional, facilita o front)
    acompanhamentos = AcompanhamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Chamado
        fields = '__all__'
        read_only_fields = ['solicitante']
    
    def get_tecnico_foto(self, obj):
        if obj.tecnico and obj.tecnico.foto_perfil:
            return obj.tecnico.foto_perfil.url
        return None