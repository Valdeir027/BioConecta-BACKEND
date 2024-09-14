from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    class Meta:
        verbose_name_plural = "Perfis" 

    nome = models.CharField(max_length=250, blank=None,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.IntegerField()


    def desativar(self):
        self.user.is_active = False
        self.user.save()
        return  self
    
    def ativar_user(self):
        self.user.is_active = True
        self.user.save()
        return self

    def __str__(self) ->str:
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=250)
    def __str__(self):
        return self.nome
    

class Professor(models.Model):

    class Meta:
        verbose_name_plural = "Professores" 
        

    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.DO_NOTHING)

    def __str__(self)->str:
        return self.perfil.nome
    