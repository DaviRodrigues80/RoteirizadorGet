# Generated by Django 5.0 on 2024-01-24 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roteirizacao_app', '0009_pagamento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('pode_add_endereco', 'Pode Adicionar Endereco'), ('pode_alterar_endereco', 'Pode Alterar Endereco'), ('pode_deletar_endereco', 'Pode Deletar Endereco')]},
        ),
        migrations.AlterModelOptions(
            name='pagamento',
            options={'permissions': [('ver_pagamento', 'Pode Ver Pagamento')]},
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data_pagamento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
