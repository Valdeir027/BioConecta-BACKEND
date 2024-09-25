from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


from .serializers import UserSerializer
from rest_framework import status
from contrib.models import Perfil
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados podem acessar

    def get(self, request):
        user = request.user  # Obtém o usuário autenticado através do token
        serializer = UserSerializer(user)  # Serializa os dados do usuário
        return Response(serializer.data)  # Retorna os dados serializados

    def post(self, request):
        
        return Response({
            "oi":"oi estou tentanto uma teoria"
        })

class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Registro de usuario",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cpf','nome','email','senha'],
            properties={
                'cpf': openapi.Schema(type=openapi.TYPE_STRING, description='CPF do usuario'),
                'nome': openapi.Schema(type=openapi.TYPE_STRING, description='Nome completo do usuario'),
                'email':openapi.Schema(type=openapi.TYPE_STRING, description='Email do usuario'),
                'senha':openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuario'),
            },
        ),
        responses={201: 'Sucesso', 409: 'Já cadastrado', 500:'Error'}
    )

    def post(self, request):
        data = request.data
        cpf = Perfil.remove_cpf_formatting(data.get('cpf'))
        nome = data.get('nome')
        email = data.get('email')
        password = data.get('senha')

        try:
            try:
                user = User.objects.get(username=cpf)
            except:
                user = None
            if user:
                return Response(status=status.HTTP_409_CONFLICT, data={
                            "Details":"CPF ja dacastrado"
                        })
            else:
                perfil = Perfil.objects.create(cpf=cpf, nome=nome)
                perfil.user.email = email
                perfil.user.set_password(password)
                perfil.user.save()

                perfil.user
                token, created = Token.objects.get_or_create(user=perfil.user)

                return Response(
                    data={
                        'cpf':perfil.cpf,
                        'first_name':perfil.user.first_name,
                        'last_name': perfil.user.last_name,
                        'auth_token':token.key,
                    },
                    status=status.HTTP_201_CREATED
                )
        except:
            return Response(status=status.is_server_error(code=500))