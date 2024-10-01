
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from bio_auth.views import custom_login, sair
from contrib.views import index


urlpatterns = [
    path('admin/', admin.site.urls, name='django_admin'),
    path('login/', custom_login, name='custom_login'),
    path('logout/', sair, name='logout'),
    path('', index, name='index')
]


#api
urlpatterns +=[
    path('api/', include('api.urls'))
]


#media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    