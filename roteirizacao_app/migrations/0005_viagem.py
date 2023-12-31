# Generated by Django 5.0 on 2024-01-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roteirizacao_app', '0004_rename_rua_endereco_logradouro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_viagem', models.CharField(max_length=50)),
                ('parada', models.CharField(max_length=50)),
                ('lougradouro', models.CharField(max_length=255)),
                ('bairro', models.CharField(max_length=255)),
                ('cidade', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
            ],
        ),
    ]
