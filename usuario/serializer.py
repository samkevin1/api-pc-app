from rest_framework import serializers
from core import models
from pedido import serializer as pedido_serializer
from rest_framework.authtoken.models import Token
from rest_framework import serializers


class UsuarioSerializer(serializers.ModelSerializer):

    pedidos = pedido_serializer.PedidoSerializer(many=True, read_only=True, source='pedido_usuario')

    class Meta:
        model = models.Usuario
        fields = ('id', 'nome', 'sobrenome', 'email', 'cpf', 'password',
                 'role', 'ativo', 'pedidos',)
        read_only_fields = ('id',)
        depth = 1


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class EmptySerializer(serializers.Serializer):
    pass