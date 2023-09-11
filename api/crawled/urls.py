from django.urls import path
from crawled import views


app_name = 'api'


urlpatterns = [
    path('', views.api_home, name='home'),
    path('process-response/', views.process_response, name='process-response'),
]
