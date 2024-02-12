# Generated by Django 5.0 on 2024-02-12 18:20

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('roteirizacao_app', '0019_delete_pagamentopix'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='Users',
        ),
        migrations.CreateModel(
            name='CustomPermissionGroup',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]