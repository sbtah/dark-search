from crawled.models import Webpage, Website
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
    def calculate_references(webpage: Webpage):
        """"""
        if webpage.number_of_references is not None:
            webpage.number_of_references += 1
        else:
            webpage.number_of_references = 1

    @staticmethod
    def calculate_response_time(webpage: Webpage, last_elapsed_seconds: str):
        """"""
        if webpage.average_response_time is not None:
            webpage.average_response_time = (webpage.average_response_time + float(last_elapsed_seconds)) / (webpage.number_of_successful_requests)
        else:
            webpage.average_response_time = float(last_elapsed_seconds)
        return webpage

    def update_or_create_webpage(
        self,
        parent_website: Website,
        url: str,
        url_after_request: str = None,
        last_http_status: str = None,
        last_elapsed: str = None,
        title: str = None,
        meta_description: str = None,
        is_file: bool = None,
        visited: int = None,
    ):
        """"""
        try:
            webpage_object = self.webpage.objects.get(
                parent_website=parent_website,
                url=url,
            )
            if url_after_request is not None:
                webpage_object.url_after_request = url_after_request
            if last_http_status is not None:
                webpage_object.last_http_status = last_http_status
                self.calculate_requests(webpage_object, last_http_status)
            if title is not None:
                webpage_object.title = title
            if meta_description is not None:
                webpage_object.meta_description = meta_description
            if is_file is not None:
                webpage_object.is_file = is_file
            if visited is not None:
                webpage_object.last_visit = visited
            if last_elapsed is not None:
                self.calculate_response_time(webpage=webpage_object, last_elapsed_seconds=last_elapsed)

            self.calculate_references(webpage_object)
            webpage_object.save()
            self.logger.info(f'Updated Webpage: {webpage_object}')
            return webpage_object
        except Webpage.DoesNotExist:

            creation_data = {
                'parent_website': parent_website,
                'url': url,
                'number_of_references': 1,
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
            if title is not None:
                creation_data['title'] = title
            if meta_description is not None:
                creation_data['meta_description'] = meta_description
            if is_file is not None:
                creation_data['is_file'] = is_file
            if visited is not None:
                creation_data['last_visit'] = visited

            webpage_object = self.webpage.objects.create(**creation_data)
            self.logger.info(f'Created new Webpage: {webpage_object}')
            return webpage_object
