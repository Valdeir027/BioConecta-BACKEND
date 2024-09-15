#python

#django
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

#local
from contrib.models import Perfil, Professor
# Create your views here.
def custom_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password = password)
        if user is not None:
            login( request=request, user=user)
            return redirect('/admin/')
        else:
            error = True  
    return render(request=request ,template_name="login.html", context={
        'error':error
    })

def create_user(request):
    error = None

    return render(request=request, template_name="create_user.html")