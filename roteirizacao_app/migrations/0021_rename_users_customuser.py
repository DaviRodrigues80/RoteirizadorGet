# Generated by Django 5.0 on 2024-02-12 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('roteirizacao_app', '0020_rename_customuser_users_custompermissiongroup'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='CustomUser',
        ),
    ]
