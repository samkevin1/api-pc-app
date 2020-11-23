from rest_framework import permissions, authentication
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from . import serializer
from core import models
from utils import response_handler, authenticate


@api_view(['GET'])
def get_all(request):
    try:
        usuario = models.Usuario.objects.filter(ativo=True)
        _serializer = serializer.UsuarioSerializer(usuario, many=True)
        return response_handler.success('Usuários ativos listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Usuario.DoesNotExist:
        return response_handler.not_found('Não há nenhum usuário ativo cadastrado no sistema.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro interno no servidor.')


@api_view(['GET'])
def get_all_disabled(request):
    try:
        usuario = models.Usuario.objects.filter(ativo=False)
        _serializer = serializer.UsuarioSerializer(usuario, many=True)
        return response_handler.success('Usuários desativados listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Usuario.DoesNotExist:
        return response_handler.not_found('Não há nenhum usuário desativado cadastrado no sistema.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['GET'])
def get_by_id(request, pk):
    try:
        usuario = models.Usuario.objects.get(id=pk, ativo=True)
        _serializer = serializer.UsuarioSerializer(usuario)
        return response_handler.success('Usuário listado com sucesso.', _serializer.data, len(_serializer.data))

    except models.Usuario.DoesNotExist:
        return response_handler.not_found('Não há nenhum usuário com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['POST'])
def create(request, *args, **kwargs):
    try:
        _serializer = serializer.UsuarioSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Usuário cadastrado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na criação do usuário', [])
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')
        

@api_view(['PATCH'])
def update(request, pk):
    try:
        usuario = models.Usuario.objects.get(id=pk)
        _serializer = serializer.UsuarioSerializer(instance=usuario, data=request.data, partial=True)

        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Usuário editado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na alteração do usuário.')

    except models.Usuario.DoesNotExist:
        return response_handler.not_found('Não há nenhum usuário com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['DELETE'])
def delete(request, pk):
    try:
        usuario = models.Usuario.objects.get(id=pk)
        usuario.ativo = False
        usuario.save()

        return response_handler.success('Usuário deletado com sucesso', [])

    except models.Usuario.DoesNotExist:
        return response_handler.not_found('O usuário não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['PATCH'])
def activate(request, pk):
    try:
        usuario = models.Usuario.objects.get(id=pk)
        usuario.ativo = True
        usuario.save()

        return response_handler.success('Usuário ativado com sucesso', [])

    except models.Usuario.DoesNotExist:
        return response_handler.not_found('O usuário não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@csrf_exempt
class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializer.EmptySerializer
    serializer_classes = {
        'login': serializer.UserLoginSerializer,
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @csrf_exempt
    @action(methods=['POST', ], detail=False)
    def login(self, request):
        _serializer = self.get_serializer(data=request.data)
        _serializer.is_valid(raise_exception=True)
        user = authenticate.get_and_authenticate_user(**_serializer.validated_data)
        data = serializer.UsuarioSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)


