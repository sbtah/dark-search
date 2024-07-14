from crawled.models.tag import Tag
from logic.adapters.base import BaseAdapter


class TagAdapter(BaseAdapter):
    """
    Adapter class
    """

    def __init__(self):
        self.tag: Tag = Tag
        super().__init__()

    def get_or_create_tag(self, value: str) -> Tag:
        """
        Create a new Tag object or return existing one.
        - :arg value: String representing a value of Tag.
        """
        try:
            existing_tag: Tag = self.tag.objects.get(value=value)
            self.logger.debug(f'TagAdapter, found existing Tag: tag_id="{existing_tag.id}", value="{value}"')
            return existing_tag
        except Tag.DoesNotExist:
            new_tag: Tag = self.tag.objects.create(value=value)
            self.logger.debug(f'TagAdapter, created new Tag: tag_id="{new_tag.id}", value="{value}"')
            return new_tag
