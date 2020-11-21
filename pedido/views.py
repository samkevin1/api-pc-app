from rest_framework import permissions, authentication
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from . import serializer
from core import models
from utils import response_handler


@api_view(['GET'])
def get_all(request):
    try:
        pedido = models.Pedido.objects.filter(ativo=True)
        _serializer = serializer.PedidoSerializer(pedido, many=True)
        return response_handler.success('Pedidos ativos listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Pedido.DoesNotExist:
        return response_handler.not_found('Não há nenhum pedido ativo cadastrado no sistema.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro interno no servidor.')


@api_view(['GET'])
def get_all_disabled(request):
    try:
        pedido = models.Pedido.objects.filter(ativo=False)
        _serializer = serializer.PedidoSerializer(pedido, many=True)
        return response_handler.success('Pedido desativados listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Pedido.DoesNotExist:
        return response_handler.not_found('Não há nenhum pedido desativado cadastrado no sistema.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['GET'])
def get_by_id(request, pk):
    try:
        pedido = models.Pedido.objects.get(id=pk, ativo=True)
        _serializer = serializer.PedidoSerializer(pedido)
        return response_handler.success('Pedido listado com sucesso.', _serializer.data, len(_serializer))

    except models.Pedido.DoesNotExist:
        return response_handler.not_found('Não há nenhum pedido com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['POST'])
def create(request, *args, **kwargs):
    try:
        _serializer = serializer.PedidoSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Pedido cadastrado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na criação do pedido', [])
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')
        

@api_view(['PATCH'])
def update(request, pk):
    try:
        pedido = models.Pedido.objects.get(id=pk)
        _serializer = serializer.PedidoSerializer(instance=pedido, data=request.data, partial=True)

        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Pedido editado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na alteração do pedido.')

    except models.Pedido.DoesNotExist:
        return response_handler.not_found('Não há nenhum pedido com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['DELETE'])
def delete(request, pk):
    try:
        pedido = models.Pedido.objects.get(id=pk)
        pedido.ativo = False
        pedido.save()

        return response_handler.success('Pedido deletado com sucesso', [])

    except models.Pedido.DoesNotExist:
        return response_handler.not_found('O pedido não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['PATCH'])
def activate(request, pk):
    try:
        pedido = models.Pedido.objects.get(id=pk)
        pedido.ativo = True
        pedido.save()

        return response_handler.success('Pedido ativado com sucesso', [])

    except models.Pedido.DoesNotExist:
        return response_handler.not_found('O pedido não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')