from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import HttpResponse, JsonResponse
import json
from libraries.adapters.webpage import WebpageAdapter
from libraries.adapters.domain import DomainAdapter


@api_view(["GET"])
def api_home(request, *args, **kwargs):
    message = {'message': 'Hi, This is Tor Search API.'}
    return JsonResponse(message)


@api_view(["POST"])
def process_response(request, *args, **kwargs):

    domain_adapter = DomainAdapter()
    webpage_adapter = WebpageAdapter()

    response_data = json.loads(request.data)

    # Extracting domain from requested url.
    requested_domain = webpage_adapter.get_domain(response_data['requested_url'])
    domain = domain_adapter.update_or_create_domain(
        domain=requested_domain,
        title=response_data.get('meta_data').get('title'),
        description=response_data.get('meta_data').get('description'),
        server=response_data.get('server'),
    )

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
            )
        return JsonResponse({'status': f'Processed successful response, for URL: {webpage.url}'})
    else:
        webpage = webpage_adapter.update_or_create_webpage(
            parent_domain=domain,
            url=response_data['requested_url'],
        )
        return JsonResponse({'status': f'Processed unsuccessful response, for URL: {webpage.url}'})
