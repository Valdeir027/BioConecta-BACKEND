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
    

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('livro_id', openapi.IN_QUERY, description="livro", type=openapi.TYPE_INTEGER),
            
        ],
        responses={200: 'Sucesso', 400: 'Erro de validação'}
    )
    def get(self, request):
        data = request.data
        book = Book.objects.get(id=data['livro_id'])
        serializer  = BookSerializer(book)

        return Response(serializer.data)
class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('titulo', openapi.IN_QUERY, description="Título do livro", type=openapi.TYPE_STRING),
            openapi.Parameter('autor', openapi.IN_QUERY, description="Nome do autor", type=openapi.TYPE_STRING),
            openapi.Parameter('estante_id', openapi.IN_QUERY, description="ID da estante", type=openapi.TYPE_INTEGER),
        ],
        responses={200: 'Sucesso', 400: 'Erro de validação'}
    )
    def get(self, request):
        # Obtém os query params da requisição
        titulo = request.query_params.get('titulo', None)
        autor = request.query_params.get('autor', None)
        estante_id = request.query_params.get('estante_id', None)

        # Inicia a query buscando todos os livros
        books = Book.objects.all()

        # Filtra por título, se o query param 'titulo' estiver presente
        if titulo:
            books = books.filter(titulo__icontains=titulo)

        # Filtra por autor, se o query param 'autor' estiver presente
        if autor:
            books = books.filter(autor__icontains=autor)

        # Filtra por estante_id, se o query param 'estante_id' estiver presente
        if estante_id:
            books = books.filter(estante__id=estante_id)

        # Serializa os dados
        serializer = BookSerializer(books, many=True)

        # Retorna a resposta com os dados filtrados
        return Response(serializer.data)



class EstanteListView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        estantes = Estante.objects.all()

        serializer = EstanteSerializer(estantes, many=True)

        return Response(serializer.data)