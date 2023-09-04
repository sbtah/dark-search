from crawled.models import Website
from libraries.adapters.base import BaseAdapter


class WebsiteAdapter(BaseAdapter):

    def __init__(self):
        self.website = Website

    def update_or_create_website(
        self,
        domain: str,
        title=None,
        description=None,
    ):
        """"""
        try:
            website_object = self.website.objects.get(
                domain=domain,
            )
            if title is not None:
                website_object.title = title
            if description is not None:
                website_object.description = description
            website_object.save()
            self.logger.info(f'Updated Website: {website_object}')
            return  website_object
        except Website.DoesNotExist:
            creation_data = {
                'domain': domain,
            }
            if title is not None:
                creation_data['title'] = title
            if description is not None:
                creation_data['description'] = description
            website_object = self.website.objects.create(**creation_data)
            self.logger.info(f'Created new Website: {website_object}')
            return website_object
