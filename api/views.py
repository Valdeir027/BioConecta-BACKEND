from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from contrib.models import Perfil
from estante.serializers import BookSerializer, EstanteSerializer
from .serializers import UserSerializer
from estante.models import Book, Estante




class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados podem acessar
    
    def get(self, request):
        user = request.user  # Obtém o usuário autenticado através do token
        serializer = UserSerializer(user)  # Serializa os dados do usuário
        return Response(serializer.data)  # Retorna os dados serializados
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
                perfil.save()
                token, created = Token.objects.get_or_create(user=perfil.user)

                return Response(
                    data={
                        'cpf':perfil.cpf,
                        'first_name':perfil.user.first_name,
                        'last_name': perfil.user.last_name,
                        'foto':perfil.foto.url,
                        'auth_token':token.key,
                        
                    },
                    status=status.HTTP_201_CREATED
                )
        except:
            return Response(status=status.is_server_error(code=500))
        



class BookView(APIView):
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem criar livros

    @swagger_auto_schema(
        operation_description="Criação de um novo livro",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['titulo', 'autor', 'estante_id'],
            properties={
                'titulo': openapi.Schema(type=openapi.TYPE_STRING, description='Título do livro'),
                'subtitulo': openapi.Schema(type=openapi.TYPE_STRING, description='Subtítulo, se houver'),
                'autor': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do autor'),
                'estante_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID da estante'),
                'descricao': openapi.Schema(type=openapi.TYPE_STRING, description='Descrição do livro'),
            },
        ),
        responses={201: 'Sucesso', 400: 'Erro de validação', 500: 'Erro interno'}
    )
    def post(self, request):
        data = request.data
        estante_id = data.get('estante_id')

        # Verificar se a estante existe
        try:
            estante = Estante.objects.get(id=estante_id)
        except Estante.DoesNotExist:
            return Response({"error": "Estante não encontrada"}, status=status.HTTP_400_BAD_REQUEST)

        # Serializar os dados e salvar
        serializer = BookSerializer(data={
            'titulo': data.get('titulo'),
            'subtitulo': data.get('subtitulo', ''),  # Subtítulo é opcional
            'autor': data.get('autor'),
            'estante': estante.id,
            'descricao': data.get('descricao', ''),  # Descrição é opcional
        })

        if serializer.is_valid():
            serializer.save()  # Salva o novo livro no banco de dados
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookListView(APIView):
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get(self, request):
        books = Book.objects.all()  # Busca todos os livros no banco de dados
        serializer = BookSerializer(books, many=True)  # Serializa os dados (many=True pois são vários livros)
        return Response(serializer.data)  # Retorna os dados serializados



class EstanteListView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        estantes = Estante.objects.all()

        serializer = EstanteSerializer(estantes, many=True)

        return Response(serializer.data)