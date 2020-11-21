from rest_framework import permissions, authentication
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from . import serializer
from core import models
from utils import response_handler


@api_view(['GET'])
def get_all(request):
    try:
        item = models.Item.objects.filter(ativo=True)
        _serializer = serializer.ItemSerializer(item, many=True)
        return response_handler.success('Itens ativos listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Item.DoesNotExist:
        return response_handler.not_found('Não há nenhum item ativo cadastrado no sistema.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro interno no servidor.')


@api_view(['GET'])
def get_all_disabled(request):
    try:
        item = models.Item.objects.filter(ativo=False)
        _serializer = serializer.ItemSerializer(item, many=True)
        return response_handler.success('Item desativados listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Item.DoesNotExist:
        return response_handler.not_found('Não há nenhum item desativado cadastrado no sistema.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['GET'])
def get_by_id(request, pk):
    try:
        item = models.Item.objects.get(id=pk, ativo=True)
        _serializer = serializer.ItemSerializer(item)
        return response_handler.success('Item listado com sucesso.', _serializer.data, len(_serializer.data))

    except models.Item.DoesNotExist:
        return response_handler.not_found('Não há nenhum item com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['POST'])
def create(request, *args, **kwargs):
    try:
        _serializer = serializer.ItemSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Item cadastrado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na criação do item', [])
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')
        

@api_view(['PATCH'])
def update(request, pk):
    try:
        item = models.Item.objects.get(id=pk)
        _serializer = serializer.ItemSerializer(instance=item, data=request.data, partial=True)

        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Item editado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na alteração do item.')

    except models.Item.DoesNotExist:
        return response_handler.not_found('Não há nenhum item com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['DELETE'])
def delete(request, pk):
    try:
        item = models.Item.objects.get(id=pk)
        item.ativo = False
        item.save()

        return response_handler.success('Item deletado com sucesso', [])

    except models.Item.DoesNotExist:
        return response_handler.not_found('O item não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['PATCH'])
def activate(request, pk):
    try:
        item = models.Item.objects.get(id=pk)
        item.ativo = True
        item.save()

        return response_handler.success('Item ativado com sucesso', [])

    except models.Item.DoesNotExist:
        return response_handler.not_found('O item não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')