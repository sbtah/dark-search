from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(["GET"])
def api_home(request, *args, **kwargs):
    message = {'message': 'Hello!'}
    return Response(message)