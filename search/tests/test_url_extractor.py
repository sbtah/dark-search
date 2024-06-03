"""
Test cases for UrlExtractor functionality.
"""
from unittest.mock import MagicMock
from urllib.parse import SplitResult

from logic.objects.url import Url
from logic.parsers.url import UrlExtractor


class TestUrlExtractor:

    def test_url_extractor_root_domain(self):
        """Test that root domain is properly set from starting_url."""
        url = Url(value='http://found.onion/')
        extractor = UrlExtractor(starting_url=url)
        assert extractor.root_domain == 'found.onion'

    def test_url_extractor_parse(self, url_extractor, urls_collection):
        """Test UrlExtractor's parse method."""
        results = url_extractor.parse(urls_collection)
        assert results == {
            'internal': {
                Url(value='http://example.onion/page.html', anchor='...', number_of_requests=0),
                Url(value='http://example.onion/page', anchor='Example Text', number_of_requests=0),
                Url(value='http://example.onion/path', anchor='Some text...', number_of_requests=0),
            },
            'external': {
                Url(value='external.onion', anchor='', number_of_requests=0),
            },
        }

    def test_url_extractor_parse_urls_collection_is_none(self, url_extractor):
        """Test that UrlExtractor's parse is returning empty parse_results."""
        raw_urls = None
        results = url_extractor.parse(raw_urls)
        assert results ==  {
            'internal': set(),
            'external': set(),
        }

    def test_url_extractor_is_valid_url_returns_true(self, url_extractor):
        """Test that UrlExtractor's is_valid_url method is returning True for proper split results."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='http', netloc='example.onion', path='/invalid.onion', query='', fragment=''
        )
        assert url_extractor.is_valid_url() is True

    def test_url_extractor_is_valid_url_returns_false(self, url_extractor):
        """Test UrlExtractor's is_valid_url method is returning False."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='', netloc='', path='/example.onion', query='', fragment=''
        )
        assert url_extractor.is_valid_url() is False

    def test_url_extractor_is_path_returns_true(self, url_extractor):
        """Test that UrlExtractor's is_path method is returning True."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='', netloc='', path='example-path', query='', fragment=''
        )
        assert url_extractor.is_path() is True

    def test_url_extractor_is_path_returns_false(self, url_extractor):
        """Test that UrlExtractor's is_path method is returning False."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='https', netloc='www.google.com', path='', query='', fragment=''
        )
        assert url_extractor.is_path() is False

    def test_url_extractor_is_onion_returns_true(self, url_extractor):
        """Test that UrlExtractor's is_onion method is returning True for onion domains."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='https', netloc='www.example.onion', path='', query='', fragment=''
        )
        assert url_extractor.is_onion() is True

    def test_url_extractor_is_onion_returns_false(self, url_extractor):
        """Test that UrlExtractor's is_onion method is returning False for other than onion domains."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='https', netloc='www.example.com', path='', query='', fragment=''
        )
        assert url_extractor.is_onion() is False

    def test_url_extractor_is_accepted_scheme_returns_true(self, url_extractor):
        """Test that UrlExtractor's is_accepted_scheme method is returning True."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='https', netloc='www.example.com', path='', query='', fragment=''
        )
        assert url_extractor.is_accepted_scheme() is True

    def test_url_extractor_is_accepted_scheme_returns_false(self, url_extractor):
        """Test that UrlExtractor's is_accepted_scheme method is returning True."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='mailto', netloc='', path='info@nofluffjobs.com', query='', fragment=''
        )
        assert url_extractor.is_accepted_scheme() is False

    def test_url_extractor_clean_url(self, url_extractor):
        """Test UrlExtractor's clean_url method."""
        test_url = Url(value='http://example.onion/p=1?v=basic', anchor='')
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='https', netloc='example.onion', path='/p=1', query='v=basic', fragment=''
        )
        assert url_extractor.clean_url(test_url) == 'http://example.onion/p=1'

    def test_url_extractor_create_url_objects(self, url_extractor, urls_collection):
        """Test that create_url_objects method is properly creating Url objects from the list of dictionaries."""
        result_list = url_extractor.create_url_objects(urls_collection)
        for result in result_list:
            assert isinstance(result, Url)
            assert isinstance(result.value, str)
            assert isinstance(result.anchor, str)
            assert isinstance(result.number_of_requests, int)
