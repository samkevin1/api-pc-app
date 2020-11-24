from rest_framework import serializers
from core import models


class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Produto
        fields = ('id', 'nome', 'vista', 'prazo', 'imagem', 'ativo', 'ram', 'placaVideo', 'processador', 'oferta')
        read_only_fields = ('id',)
        depth = 1
