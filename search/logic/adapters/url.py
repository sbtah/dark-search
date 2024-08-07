from typing import Any

from logic.adapters.base import BaseAdapter
from logic.exceptions.adapters.url import (
    WrongTypeProvidedError,
    WrongValueProvidedError
)
from logic.objects.url import Url


class UrlAdapter(BaseAdapter):
    """
    Adapter class for Url objects.
    The Main purpose of this class is to help in creating new objects
        and validating inputs.
    """

    def __init___(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_url_object(
        value: str, anchor: str | None = None, number_of_requests: int | None = None
    ) -> Url:
        """
        Create a single Url object.
        Validate values provided for attributes.
        - :arg href: String with Url value.
        - :arg anchor: String with anchor text.
        - :arg number_of_requests: Integer representing number of requests.
        """
        if not isinstance(value, str):
            raise WrongTypeProvidedError()

        # The Shortest possible url is 3 characters, but we deal with onion domains.
        if len(value) < 6:
            raise WrongValueProvidedError()

        if anchor is not None and not isinstance(anchor, str):
            raise WrongTypeProvidedError()

        if number_of_requests is not None and not isinstance(number_of_requests, int):
            raise WrongTypeProvidedError()

        creation_data: dict = {
            'value': value
        }
        if anchor is not None:
            creation_data['anchor'] = anchor
        if number_of_requests is not None:
            creation_data['number_of_requests'] = number_of_requests

        return Url(**creation_data)
