from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    nome = models.CharField(max_length=250, blank=None,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.IntegerField()

    
    def __str__(self) ->str:
        return self.nome

class Disciplinas(models.Model):
    nome = models.CharField(max_length=250)
    
    def __str__(self):
        return self.nome
    

class Professor(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.DO_NOTHING)
    