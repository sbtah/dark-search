from libraries.adapters.base import BaseAdapter
from crawled.models import Webpage, Website


class WebpageAdapter(BaseAdapter):

    def __init__(self):
        self.webpage = Webpage

    def update_or_create_webpage(
        self,
        parent_website: Website,
        url: str,
        title: str = None,
        description: str = None,
        is_file: bool = None,
        number_of_references: int = None,
        last_visit: int = None,
        is_active: bool = None,
    ):
        """"""
        try:
            webpage_object = self.webpage.objects.get(
                parrent_website=parent_website,
                url=url,
            )
            if title is not None:
                webpage_object.title = title
            if description is not None:
                webpage_object.description = description
            if is_file is not None:
                webpage_object.is_file = is_file
            if number_of_references is not None:
                webpage_object.number_of_references = number_of_references
            if last_visit is not None:
                webpage_object.last_visit = last_visit
            if is_active is not None:
                webpage_object.is_active = is_active
            webpage_object.save()
            self.logger.info(f'Created new Webpage: {webpage_object}')
            return webpage_object
        except Webpage.DoesNotExist:
            creation_data = {
                'parent_website': parent_website,
                'url': url,
            }
            if title is not None:
                creation_data['title'] = title
            if description is not None:
                creation_data['description'] = description
            if is_file is not None:
                creation_data['is_file'] = is_file
            if number_of_references is not None:
                creation_data['number_of_references'] = number_of_references
            if last_visit is not None:
                creation_data['last_visit'] = last_visit
            if is_active is not None:
                creation_data['is_active'] = last_visit
            webpage_object = self.webpage.objects.create(**creation_data)
            self.logger.info(f'Updated Webpage: {webpage_object}')
            return webpage_object
