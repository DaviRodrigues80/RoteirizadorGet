# Generated by Django 5.0 on 2024-02-07 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roteirizacao_app', '0011_alter_pagamento_valido_ate'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='quant_acesso',
            field=models.DateField(blank=True, null=True),
        ),
    ]