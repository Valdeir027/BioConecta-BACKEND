
from django.contrib import admin
from django.urls import path
from bio_auth.views import custom_login
urlpatterns = [
    path('admin/', admin.site.urls, name='django_admin'),
    path('login/', custom_login, name='custom_login')
]
