from rest_framework import serializers 
from core import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ('id', 'valor_item', 'quantidade_item', 'ativo', 'produto', 'pedido',)
        read_only_fields = ('id',)