from django.db import models
from django.forms import forms


class Produto(models.Model):
    nome = models.CharField(max_length=32)
    vista = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    prazo = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    imagem = models.CharField(max_length=128)
    ativo = models.BooleanField(default=True)
    ram = models.CharField(max_length=32, null=True)
    placaVideo = models.CharField(max_length=32, null=True)
    processador = models.CharField(max_length=32, null=True)


class Usuario(models.Model):
    nome = models.CharField(max_length=32)
    sobrenome = models.CharField(max_length=32)
    email = models.EmailField()
    cpf = models.CharField(max_length=11)
    password = models.CharField(max_length=64)
    role = models.CharField(max_length=12)
    ativo = models.BooleanField(default=True)


class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='pedido_usuario', on_delete=models.CASCADE)
    status = models.CharField(max_length=32)
    valor_total = models.DecimalField(max_digits=5, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)


class Item(models.Model):
    produto = models.ForeignKey(Produto, related_name="item_produto", on_delete=models.CASCADE, default=0)
    pedido = models.ForeignKey(Pedido, related_name="item_pedido", on_delete=models.CASCADE, default=0)
    valor_item = models.DecimalField(max_digits=5, decimal_places=2)
    quantidade_item = models.IntegerField()
    ativo = models.BooleanField(default=True)
