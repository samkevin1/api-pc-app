from rest_framework import serializers
from core import models
from item import serializer as item_serializer


class PedidoSerializer(serializers.ModelSerializer):

    itens = item_serializer.ItemSerializer(many=True, read_only=True, source="item_pedido")

    class Meta:
        model = models.Pedido
        fields = ('id', 'status', 'valor_total', 'data_pedido', 'ativo', 'usuario', 'itens',)
        read_only_fields = ('id',)
