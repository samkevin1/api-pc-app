from rest_framework import serializers
from core import models
from pedido import serializer as pedido_serializer
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class UsuarioSerializer(serializers.ModelSerializer):

    pedidos = pedido_serializer.PedidoSerializer(many=True, read_only=True, source='pedido_usuario')

    class Meta:
        model = models.User
        fields = ('id', 'nome', 'sobrenome', 'email', 'cpf', 'password',
                 'role', 'ativo', 'pedidos',)
        read_only_fields = ('id',)
        depth = 1

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
