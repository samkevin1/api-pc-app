from rest_framework import serializers
from core import models
from produto import serializer as produto_serializer


class PedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Pedido
        fields = ('id', 'valor_total', 'data_pedido', 'ativo', 'usuario', 'produtos',)
        read_only_fields = ('id',)