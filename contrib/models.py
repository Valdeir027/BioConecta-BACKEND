from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    nome = models.CharField(max_length=250, blank=None,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
    
    def __str__(self) ->str:
        return self.nome