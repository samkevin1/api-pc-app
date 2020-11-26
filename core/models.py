from django.contrib.auth.hashers import make_password
from django.db import models
from django.forms import forms
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, nome, sobrenome, cpf, senha,):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, cpf=cpf, sobrenome=sobrenome, senha=senha)

        user.set_password(senha)
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
    senha = models.CharField(max_length=250)
    role = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Produto(models.Model):
    nome = models.CharField(max_length=32)
    vista = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    prazo = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    imagem = models.CharField(max_length=1000)
    ativo = models.BooleanField(default=True)
    ram = models.CharField(max_length=32, null=True)
    placaVideo = models.CharField(max_length=32, null=True)
    processador = models.CharField(max_length=32, null=True)
    oferta = models.BooleanField(default=False)


class Pedido(models.Model):
    usuario = models.ForeignKey(User, related_name='pedido_usuario', on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto)
    valor_total = models.DecimalField(max_digits=7, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
