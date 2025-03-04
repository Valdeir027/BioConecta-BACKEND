#python

#django
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#local
from contrib.models import Perfil
from contrib.views import index
from contrib.models import Perfil


# Create your views here.
def custom_login(request):
    error = None
    text_error = ''
    next_url = request.GET.get('next', 'index')
    if request.method == 'POST':
        if request.POST.get('form') =='loginForm':
            username = Perfil.remove_cpf_formatting(request.POST.get('username'))
            password = request.POST.get('password')

            user = authenticate(request=request, username=username, password = password)
            if user is not None:
                login( request=request, user=user)
                return redirect(next_url)
            else:
                error = True
                text_error = "Cpf ou senha inválidos"
        if request.POST.get('form') == 'cadastroForm':
            user = None
            nome = request.POST.get('nome')
            cpf = Perfil.remove_cpf_formatting(request.POST.get('cpf'))
            email = request.POST.get('email')
            senha1 = request.POST.get('password')
            senha2 = request.POST.get('password2')
            try:
                user = User.objects.get(username=cpf)
            except:
                user = None

            if user is None:
                if senha1 == senha2:
                    perfil = Perfil.objects.create(nome=nome, cpf=cpf)
                    perfil.user.set_password(senha1)
                    perfil.user.email = email
                    perfil.user.save()
                    perfil.save()
                    
                    authenticate(perfil.user, senha1)
                    login(user=perfil.user, request=request)
                    print(perfil.foto)
                    return redirect(next_url)
                else:
                    error = True
                    text_error = 'As senhas não conferem'
            else:
                error = True
                text_error='Cpf ja cadastrado'

            
                
    return render(request=request ,template_name="login.html", context={
        'error':error,
        'textError':text_error
    })

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/login')
