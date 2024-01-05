from django.db import models


# Tabela Endereco
class Endereco(models.Model):
    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)


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
