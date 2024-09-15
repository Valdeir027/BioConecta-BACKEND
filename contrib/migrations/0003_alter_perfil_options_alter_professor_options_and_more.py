# Generated by Django 5.1.1 on 2024-09-15 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contrib', '0002_rename_disciplinas_disciplina'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfil',
            options={'verbose_name_plural': 'Perfis'},
        ),
        migrations.AlterModelOptions(
            name='professor',
            options={'verbose_name_plural': 'Professores'},
        ),
        migrations.AddField(
            model_name='perfil',
            name='cpf',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
