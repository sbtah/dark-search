from crawled.models import Webpage, Domain
from libraries.adapters.base import BaseAdapter


class WebpageAdapter(BaseAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webpage = Webpage

    @staticmethod
    def calculate_requests(webpage: Webpage, last_http_status: str):
        """"""
        if last_http_status.startswith('2') or last_http_status.startswith('3'):
            if webpage.number_of_successful_requests is not None:
                webpage.number_of_successful_requests += 1
            else:
                webpage.number_of_successful_requests = 1
        else:
            if webpage.number_of_unsuccessful_requests is not None:
                webpage.number_of_unsuccessful_requests += 1
            else:
                webpage.number_of_unsuccessful_requests = 1
        return webpage

    @staticmethod
    def calculate_response_time(webpage: Webpage, last_elapsed_seconds: str):
        """"""
        if webpage.average_response_time is not None:
            webpage.average_response_time = (webpage.average_response_time + float(last_elapsed_seconds)) / (webpage.number_of_successful_requests if webpage.number_of_successful_requests is not None else 1)
        else:
            webpage.average_response_time = float(last_elapsed_seconds)
        return webpage

    def update_or_create_webpage(
        self,
        parent_domain: Domain,
        url: str,
        url_after_request: str = None,
        last_http_status: str = None,
        # For calculating average_response_time
        last_elapsed: str = None,
        raw_html: str = None,
        page_title: str = None,
        meta_title: str = None,
        meta_description: str = None,
        on_page_raw_urls: list = None,
        on_page_processed_urls: list = None,
        last_visit: int = None,
    ):
        """"""
        try:
            webpage_object = self.webpage.objects.get(
                parent_domain=parent_domain,
                url=url,
            )
            if url_after_request is not None:
                webpage_object.url_after_request = url_after_request
            if last_http_status is not None:
                webpage_object.last_http_status = last_http_status
                webpage_object = self.calculate_requests(webpage_object, last_http_status)
            if raw_html is not None:
                webpage_object.raw_html = raw_html
            if page_title is not None:
                webpage_object.page_title = page_title
            if meta_title is not None:
                webpage_object.meta_title = meta_title
            if meta_description is not None:
                webpage_object.meta_description = meta_description
            if last_elapsed is not None:
                webpage_object = self.calculate_response_time(webpage=webpage_object, last_elapsed_seconds=last_elapsed)
            if on_page_raw_urls is not None:
                webpage_object.on_page_raw_urls = on_page_raw_urls
            if on_page_processed_urls is not None:
                webpage_object.on_page_processed_urls = on_page_processed_urls
            if last_visit is not None:
                webpage_object.last_visit = last_visit

            webpage_object.save()
            self.logger.debug(f'Updated Webpage: {webpage_object}')
            return webpage_object
        except Webpage.DoesNotExist:

            creation_data = {
                'parent_domain': parent_domain,
                'url': url,
            }
            if url_after_request is not None:
                creation_data['url_after_request'] = url_after_request
            if last_http_status is not None:
                creation_data['last_http_status'] = last_http_status
                if last_http_status.startswith('2') or last_http_status.startswith('3'):
                    creation_data['number_of_successful_requests'] = 1
                    creation_data['is_active'] = True
                else:
                    creation_data['number_of_unsuccessful_requests'] = 1
                    creation_data['is_active'] = False
            if last_elapsed is not None:
                creation_data['average_response_time'] = last_elapsed
            if raw_html is not None:
                creation_data['raw_html'] = raw_html
            if page_title is not None:
                creation_data['page_title'] = page_title
            if meta_title is not None:
                creation_data['meta_title'] = meta_title
            if meta_description is not None:
                creation_data['meta_description'] = meta_description
            if on_page_raw_urls is not None:
                creation_data['on_page_raw_urls'] = on_page_raw_urls
            if on_page_processed_urls is not None:
                creation_data['on_page_processed_urls'] = on_page_processed_urls
            if last_visit is not None:
                creation_data['last_visit'] = last_visit

            webpage_object = self.webpage.objects.create(**creation_data)
            self.logger.debug(f'Created new Webpage: {webpage_object}')
            return webpage_object
