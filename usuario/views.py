from rest_framework import permissions, authentication
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from . import serializer
from core import models
from utils import response_handler, authenticate


@api_view(['GET'])
def get_all(request):
    try:
        usuario = models.User.objects.filter(ativo=True)
        _serializer = serializer.UsuarioSerializer(usuario, many=True)
        return response_handler.success('Usuários ativos listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.User.DoesNotExist:
        return response_handler.not_found('Não há nenhum usuário ativo cadastrado no sistema.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro interno no servidor.')


@api_view(['GET'])
def get_all_disabled(request):
    try:
        usuario = models.User.objects.filter(ativo=False)
        _serializer = serializer.UsuarioSerializer(usuario, many=True)
        return response_handler.success('Usuários desativados listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.User.DoesNotExist:
        return response_handler.not_found('Não há nenhum usuário desativado cadastrado no sistema.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['GET'])
def get_by_id(request, pk):
    try:
        usuario = models.User.objects.get(id=pk, ativo=True)
        _serializer = serializer.UsuarioSerializer(usuario)
        return response_handler.success('Usuário listado com sucesso.', _serializer.data, len(_serializer.data))

    except models.User.DoesNotExist:
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
        usuario = models.User.objects.get(id=pk)
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
        usuario = models.User.objects.get(id=pk)
        usuario.ativo = False
        usuario.save()

        return response_handler.success('Usuário deletado com sucesso', [])

    except models.User.DoesNotExist:
        return response_handler.not_found('O usuário não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['PATCH'])
def activate(request, pk):
    try:
        usuario = models.User.objects.get(id=pk)
        usuario.ativo = True
        usuario.save()

        return response_handler.success('Usuário ativado com sucesso', [])

    except models.User.DoesNotExist:
        return response_handler.not_found('O usuário não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


class CreateTokenView(ObtainAuthToken):

    serializer_class = serializer.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):

        _serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        _serializer.is_valid(raise_exception=True)
        user = _serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        _user = models.User.objects.get(email__exact=user.email)
        __serializer = serializer.UsuarioSerializer(instance=_user)
        return Response({'success': True, 'message': 'Usuário logado com sucesso!', 'token': token.key, 'data': __serializer.data})
