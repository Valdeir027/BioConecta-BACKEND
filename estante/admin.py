from django.contrib import admin
from .models import Book, Estante
from django.utils.html import format_html


class BookAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'estante','descricao')

    def icone(self, obj):
        # Use FontAwesome ícones
        return format_html('<i class="fas fa-book"></i>')
    



admin.site.register(Book, BookAdmin)
admin.site.register(Estante)