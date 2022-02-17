from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-static-files-during-development

# Конфигурация сайта/страницы/приложения админа с помощью атрибутов
# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#adminsite-attributes
admin.site.site_header = "My Club Administration"
admin.site.site_title = "Adminka"
admin.site.index_title = "Welcome to Admin"