from django.contrib import admin
from .models import Perfil,Disciplina, Professor

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class PerfilInline(admin.StackedInline):  # Ou use TabularInline para layout tabular
    model = Perfil
    can_delete = False  # Impede a exclusão do perfil diretamente
    verbose_name_plural = 'perfis'


# Opção 1: Extender o UserAdmin para adicionar o Perfil
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Re-registra o UserAdmin com o novo inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Disciplina)
admin.site.register(Professor)