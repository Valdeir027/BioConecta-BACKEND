from django.db import models
from django.contrib.auth.models import User
import re

# Create your models here.
class Perfil(models.Model):
    class Meta:
        verbose_name_plural = "Perfis" 

    nome = models.CharField(max_length=250, blank=None,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)

    foto = models.ImageField( upload_to='perfil_pics', default='defaultUserPerfil.png')

    def first_name(self):
        return self.nome.split(' ')[0]
    
    def last_name(self):
        self.nome.split(' ')[1:]
        return ' '.join(self.nome.split(' ')[1:])

    def remove_cpf_formatting(cpf):
        # Remove qualquer caractere que não seja dígito usando expressões regulares
        cpf_clean = re.sub(r'\D', '', cpf) 
        return cpf_clean

    def desativar(self):
        self.user.is_active = False
        self.user.save()
        return  self
    
    def ativar_user(self):
        self.user.is_active = True
        self.user.save()
        return self
    

    def save(self, *args, **kwargs):
        # Se não houver um usuário associado, cria um novo usuário automaticamente
        if not self.user_id:
            self.user = User.objects.create(
                first_name=self.first_name(),
                last_name = self.last_name(),
                username=self.cpf,
                )

        # Chama o método original de salvamento
        super(Perfil, self).save(*args, **kwargs)
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
    