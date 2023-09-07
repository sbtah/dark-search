from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from crawled.models import Webpage, Website
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from libraries.adapters.webpage import WebpageAdapter
from libraries.adapters.website import WebsiteAdapter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def api_home(request, *args, **kwargs):
    message = {'message': 'Hi, This is Tor Search API.'}
    return JsonResponse(message)



@api_view(["POST"])
def process_response(request, *args, **kwargs):

    website_adapter = WebsiteAdapter()
    webpage_adapter = WebpageAdapter()

    response_data = json.loads(request.data)

    # Extracting domain from requested url.
    requested_domain = webpage_adapter.get_domain(response_data['requested_url'])
    website = website_adapter.update_or_create_website(
        domain=requested_domain,
        server=response_data.get('server'),
    )

    if response_data['status'] is not None:
        webpage = webpage_adapter.update_or_create_webpage(
            parent_website=website,
            url=response_data['requested_url'],
            url_after_request=response_data['responded_url'],
            last_http_status=response_data['status'],
            last_elapsed=response_data['elapsed'],
            title=response_data['meta_data']['title'],
            meta_description=response_data['meta_data']['description'],
            is_file=response_data['is_file'],
            visited=response_data['visited'],
            )
        return JsonResponse({'status': f'Processed successful response, for URL: {webpage.url}'})
    else:
        webpage = webpage_adapter.update_or_create_webpage(
            parent_website=website,
            url=response_data['requested_url'],
        )
        return JsonResponse({'status': f'Processed unsuccessful response, for URL: {webpage.url}'})