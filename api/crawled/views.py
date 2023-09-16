import json

from django.http import JsonResponse
from libraries.adapters.domain import DomainAdapter
from libraries.adapters.webpage import WebpageAdapter
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view(["GET"])
def api_home(request, *args, **kwargs):
    message = {'message': 'Hi, This is Tor Search API.'}
    return JsonResponse(message)


@api_view(["POST"])
def process_response(request, *args, **kwargs):

    domain_adapter = DomainAdapter()
    webpage_adapter = WebpageAdapter()

    response_data = json.loads(request.data)
    print(f'DEBUG DATA: {response_data}')
    # Extracting domain from requested url.
    requested_domain = webpage_adapter.get_domain(
        response_data['requested_url'],
    )
    domain = domain_adapter.update_or_create_domain(
        domain=requested_domain,
        title=response_data.get('meta_data').get('title') if response_data.get('meta_data') is not None else None,
        description=response_data.get('meta_data').get('description') if response_data.get('meta_data') is not None else None,
        server=response_data.get('server'),
    )
    print(f'DEBUG API DOMAIN OBJECT: {domain}')

    if response_data['status'] is not None:
        webpage = webpage_adapter.update_or_create_webpage(
            parent_domain=domain,
            url=response_data['requested_url'],
            url_after_request=response_data['responded_url'],
            last_http_status=response_data['status'],
            last_elapsed=response_data['elapsed'],
            title=response_data['meta_data']['title'],
            meta_description=response_data['meta_data']['description'],
            visited=response_data['visited'],
            on_page_raw_urls=response_data['raw_urls'],
            on_page_processed_urls=response_data['processed_urls']

        )
        return JsonResponse(
            {'status': f'Parsed response: {webpage.url}'}
        )
    else:
        webpage = webpage_adapter.update_or_create_webpage(
            parent_domain=domain,
            url=response_data['requested_url'],
        )
        return JsonResponse(
            {'status': f'Parsed empty response: {webpage.url}'}
        )
