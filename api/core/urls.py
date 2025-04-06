from core.api import api
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Url Patterns.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
