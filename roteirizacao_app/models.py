from django.db import models

class Endereco(models.Model):
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
