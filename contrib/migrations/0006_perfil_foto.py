# Generated by Django 5.1.1 on 2024-09-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contrib', '0005_alter_perfil_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='foto',
            field=models.ImageField(default='perfil_pics/default.jpg', upload_to='perfil_pics'),
        ),
    ]
