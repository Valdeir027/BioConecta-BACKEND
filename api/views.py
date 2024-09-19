from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework import status
from contrib.models import Perfil

from django.contrib.auth import authenticate, login
from .serializers import UserCreateSerializer, PerfilSerializer

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
    def post(self, request):
        user_serializer = UserCreateSerializer(data=request.data)
        perfil_serializer = PerfilSerializer(data=request.data)

        if user_serializer.is_valid() and perfil_serializer.is_valid():
            user = user_serializer.save()
            perfil = perfil_serializer.save(user=user)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        errors = {**user_serializer.errors, **perfil_serializer.errors}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)