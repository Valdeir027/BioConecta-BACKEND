from django.shortcuts import render
from .models import *

# Create your views here.
def index(request): # Pagina home para visualização do livro
    return render(request, "estante/index.html")