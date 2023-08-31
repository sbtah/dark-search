from django.contrib import admin
from django.urls import path, include
from crawled import views


app_name = 'api'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_home, name='home'),
]
