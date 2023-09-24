import json

from django.http import JsonResponse
from libraries.adapters.domain import DomainAdapter
from libraries.adapters.webpage import WebpageAdapter
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view(['GET'])
def api_home(request, *args, **kwargs):
    """"""
    message = {'message': 'Hi, This is Tor Search API.'}
    return JsonResponse(message)


@api_view(['POST'])
def process_response(request, *args, **kwargs):
    """
    Process incoming response data from crawlers.
    """

    domain_adapter = DomainAdapter()
    webpage_adapter = WebpageAdapter()

    response_data = json.loads(request.data)
    # Extracting domain from requested url.
    requested_domain = webpage_adapter.get_domain(
        response_data['requested_url'],
    )
    domain = domain_adapter.update_or_create_domain(
        value=requested_domain,
        server=response_data.get('server'),
    )
    try:
        if response_data['status'] is not None:
            webpage = webpage_adapter.update_or_create_webpage(
                parent_domain=domain,
                url=response_data['requested_url'],
                url_after_request=response_data['responded_url'],
                last_http_status=response_data['status'],
                last_elapsed=response_data['elapsed'],
                raw_html=response_data['raw_html'],
                page_title=response_data['page_title'],
                meta_title=response_data['meta_data']['title'],
                meta_description=response_data['meta_data']['description'],
                last_visit=response_data['visited'],
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
    except Exception as e:
        return JsonResponse(
                {'status': f'Exception in view: {e}'}
            )

@api_view(['POST'])
def process_summary(request, *args, **kwargs):
    """
    Process summary data after finished crawling.
    """

    domain_adapter = DomainAdapter()
    response_data = json.loads(request.data)

    domain = domain_adapter.update_or_create_domain(
        value=response_data['domain'],
        last_crawl_date=response_data['date'],
        last_crawl_time=response_data['time'],
        number_of_pages_found=response_data['urls_crawled'],
        number_of_crawls_finished=1
    )
    return JsonResponse({'status': f'Updated {domain}'})