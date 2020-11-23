from django.db import models
from django.forms import forms
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class Produto(models.Model):
    nome = models.CharField(max_length=32)
    vista = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    prazo = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    imagem = models.CharField(max_length=128)
    ativo = models.BooleanField(default=True)
    ram = models.CharField(max_length=32, null=True)
    placaVideo = models.CharField(max_length=32, null=True)
    processador = models.CharField(max_length=32, null=True)


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, nome, sobrenome, cpf, password=None,):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, cpf=cpf, sobrenome=sobrenome)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nome, password):
        """Create and save a new superuser with given details"""
        user = self.model(email=email, name=nome)

        user.set_password(password)
        user.is_superuser = True
        user.role = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    nome = models.CharField(max_length=32)
    sobrenome = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11)
    password = models.CharField(max_length=250)
    role = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Pedido(models.Model):
    usuario = models.ForeignKey(User, related_name='pedido_usuario', on_delete=models.CASCADE)
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
