from rest_framework import serializers
from .models import Book, Estante

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'titulo', 'subtitulo', 'autor', 'estante', 'descricao']

class EstanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estante
        fields = ['id', 'nome']