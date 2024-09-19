from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contrib.models import Perfil

# Create your views here.
@login_required
def index(request):
    if not request.user.is_authenticated:
        # Lidar com a situação onde o usuário não está autenticado
        return redirect('login')  # Redireciona para a página de login ou outra ação apropriada

    try:
        perfil = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        # Lidar com a situação onde o perfil não existe
        perfil = None

    return render(request, template_name="desenvolvendo.html", context={
        'user': request.user,
        'nome_usuario': perfil.first_name() if perfil else 'Nome não disponível'
    })