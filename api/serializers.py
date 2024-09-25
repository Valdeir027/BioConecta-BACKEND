from rest_framework import serializers
from django.contrib.auth.models import User
from contrib.models import Perfil  # Supondo que você tenha um modelo Perfil

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
