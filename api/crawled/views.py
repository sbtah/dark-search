from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from crawled.models import Webpage, Website
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from libraries.adapters.webpage import WebpageAdapter
from libraries.adapters.website import WebsiteAdapter


@api_view(["GET"])
def api_home(request, *args, **kwargs):
    message = {'message': 'Hi, This is Tor Search API.'}
    return JsonResponse(message)


@api_view(["POST"])
def process_urls(request, *args, **kwargs):

    website_adapter = WebsiteAdapter()
    webpage_adapter = WebpageAdapter()

    urls_data = json.loads(request.data)
    if urls_data['urls']:
        for url in urls_data['urls']:
            domain = webpage_adapter.get_domain(url)
            website = website_adapter.update_or_create_website(domain)
            webpage = webpage_adapter.update_or_create_webpage(parent_website=domain, url=url)
        return JsonResponse({'status': 'Processed'})
    else:
        return JsonResponse({'status': 'Received no URLS to process.'})
