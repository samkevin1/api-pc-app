from rest_framework import permissions, authentication
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from . import serializer
from core import models
from utils import response_handler


@api_view(['GET'])
def get_all(request):
    try:
        produto = models.Produto.objects.filter(ativo=True)
        _serializer = serializer.ProdutoSerializer(produto, many=True)
        return response_handler.success('Produtos ativos listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Produto.DoesNotExist:
        return response_handler.not_found('Não há nenhum produto ativo cadastrado no sistema.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro interno no servidor.')


@api_view(['GET'])
def get_all_disabled(request):
    try:
        produto = models.Produto.objects.filter(ativo=False)
        _serializer = serializer.ProdutoSerializer(produto, many=True)
        return response_handler.success('Produtos desativados listados com sucesso.', _serializer.data, len(_serializer.data))

    except models.Produto.DoesNotExist:
        return response_handler.not_found('Não há nenhum produto desativado cadastrado no sistema.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['GET'])
def get_by_id(request, pk):
    try:
        produto = models.Produto.objects.get(id=pk, ativo=True)
        _serializer = serializer.ProdutoSerializer(produto)
        return response_handler.success('Produto listado com sucesso.', _serializer.data, len(_serializer.data))

    except models.Produto.DoesNotExist:
        return response_handler.not_found('Não há nenhum produto com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['POST'])
def create(request, *args, **kwargs):
    try:
        _serializer = serializer.ProdutoSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Produto cadastrado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na criação do produto', [])
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')
        

@api_view(['PATCH'])
def update(request, pk):
    try:
        produto = models.Produto.objects.get(id=pk)
        _serializer = serializer.ProdutoSerializer(instance=produto, data=request.data, partial=True)

        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return response_handler.success('Produto editado com sucesso.', _serializer.data)
        else:
            return response_handler.error_has_ocurred('Ocorreu um erro na alteração do produto.')

    except models.Produto.DoesNotExist:
        return response_handler.not_found('Não há nenhum produto com esse id.')

    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['DELETE'])
def delete(request, pk):
    try:
        produto = models.Produto.objects.get(id=pk)
        produto.ativo = False
        produto.save()

        return response_handler.success('Cardápio deletado com sucesso', [])

    except models.Produto.DoesNotExist:
        return response_handler.not_found('O produto não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')


@api_view(['PATCH'])
def activate(request, pk):
    try:
        produto = models.Produto.objects.get(id=pk)
        produto.ativo = True
        produto.save()

        return response_handler.success('Produto ativado com sucesso', [])

    except models.Produto.DoesNotExist:
        return response_handler.not_found('O produto não foi encontrado.')
    
    except RuntimeError:
        raise RuntimeError('Ocorreu um erro no sistema.')