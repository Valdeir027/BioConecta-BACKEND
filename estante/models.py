from django.db import models

class Estante(models.Model):
    nome = models.CharField(max_length=250, blank=False, null=True)
    

    def __str__(self) -> str:
        return self.nome
    


class Book(models.Model):
    titulo = models.CharField(max_length=250)
    subtitulo = models.CharField(max_length=500, blank=True, null=True)
    autor = models.CharField(max_length=250)

    estante = models.ForeignKey(Estante, on_delete=models.DO_NOTHING)

    descricao = models.TextField()

