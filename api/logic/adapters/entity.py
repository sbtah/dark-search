from logic.adapters.base import BaseAdapter
from crawled.models import Entity


class EntityAdapter(BaseAdapter):
    """
    Adapter class for managing Entity objects.
    """

    def __init__(self) -> None:
        self.entity: Entity = Entity
        super().__init__()

    def sync_get_or_create_entity(
        self,
        name: str,
        description: str | None = None,
        additional_data: dict | None = None,
    ) -> Entity:
        """
        Synchnronous version.
        Create new Entity object or return existing one.
        Return Entity object.
        - :arg name: String representing Entity name.
        - :arg description: String representing extra description about Entity.
        - :arg additional_data: Dictionary with any extra data about Entity
        """
        try:
            existing_entity: Entity = self.entity.objects.get(name=name)
            self.logger.debug(f'EntityAdapter, found existing Entity: entity_id="{existing_entity.id}", name="{name}"')
            return existing_entity
        except Entity.DoesNotExist:
            creation_data: dict = {'name': name}
            if description is not None:
                creation_data['description'] = description
            if additional_data is not None:
                creation_data['additional_data'] = additional_data
            new_entity: Entity = self.entity.objects.create(**creation_data)
            self.logger.debug(f'EnityAdapter, created new Entity: entity_id="{new_entity.id}", name="{name}"')
            return new_entity

