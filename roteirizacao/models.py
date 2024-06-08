from django import forms
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, User
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de e-mail deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    choices_cargo = (
        ('U', 'Usuario'),
        ('Admin', 'Administrador'),
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=5, choices=choices_cargo)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    def delete(self, using=None, keep_parents=False):
        # Substituímos o método delete padrão para realizar um soft delete
        self.is_active = False
        self.save()

    # Adicione o related_name aqui
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.cargo:
            self.cargo = 'U'  # Define um valor padrão para o cargo caso não seja especificado

    class Meta:
        permissions = [
            ("pode_add_endereco", "Pode Adicionar Endereco"),
            ("pode_alterar_endereco", "Pode Alterar Endereco"),
            ("pode_deletar_endereco", "Pode Deletar Endereco"),
            # Adicione permissões adicionais conforme necessário
        ]


# Tabela Endereco
class Endereco(models.Model):
    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    estado = models.CharField(max_length=50)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return f"{self.cep}, {self.logradouro}, {self.bairro}, {self.cidade}, {self.numero}, {self.estado}, {self.latitude}, {self.longitude} "

# Tabela Viagem
class Viagem(models.Model):
    numero_viagem = models.CharField(max_length=50)
    parada = models.CharField(max_length=50)
    lougradouro = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)



# Gerencia Pagementos
CustomUser = get_user_model()

class Pagamento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use settings.AUTH_USER_MODEL
    codigo_pagamento = models.CharField(max_length=30, null=True)
    data_pagamento = models.DateField(null=True, blank=True)
    valido_ate = models.DateField(null=True, blank=True)
    quant_acesso = models.IntegerField(default=0)

    class Meta:
        permissions = [
            ("ver_pagamento", "Pode Ver Pagamento"),
            # Adicione permissões adicionais conforme necessário
        ]


class PagamentoForm(forms.ModelForm):
    # Define o campo de busca para selecionar uma instância existente do modelo Pagamento
    pagamento = forms.ModelChoiceField(
        queryset=Pagamento.objects.all(),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pesquisar pagamento'}),
        required=False
    )

    class Meta:
        model = Pagamento
        fields = '__all__'

    # Inclui a lógica para salvar a instância selecionada do pagamento se ela existir
    def save(self, commit=True):
        pagamento = self.cleaned_data.get('pagamento')
        if pagamento:
            return pagamento
        return super().save(commit=commit)

## Gerenciar Permissões - INICIO
class CustomPermissionGroup(Group):
    class Meta:
        proxy = True

## Gerenciar Permissões - FIM
