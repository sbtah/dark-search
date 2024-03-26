from unittest.mock import MagicMock
from urllib.parse import SplitResult

from logic.parsers.url import UrlExtractor


class TestUrlExtractor:

    def test_url_extractor_root_domain(self):
        """Test that root domain is properly set from starting_url."""
        extractor = UrlExtractor(starting_url='http://found.onion/')
        assert extractor.root_domain == 'found.onion'

    def test_url_extractor_parse(self, url_extractor):
        """Test UrlExtractor's parse method."""
        results = url_extractor.parse()
        assert results == {
            'internal': {'http://example.onion/page', 'http://example.onion/path'},
            'external': {'http://external.onion/'}
        }

    def test_is_valid_url_returns_true(self, url_extractor):
        """Test that UrlExtractor's is_valid_url method is returning True for proper split results."""
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='http', netloc='example.onion', path='/invalid.onion', query='', fragment=''
        )
        assert url_extractor.is_valid_url() is True

    def test_is_valid_url_returns_false(self, url_extractor):
        """Test UrlExtractor's is_valid_url method is returning False."""
        url_extractor.current_url_split_result = MagicMock(
            scheme='', netloc='', path='example.onion', query='', fragment=''
        )
        assert url_extractor.is_valid_url() is False

    def test_is_path_returns_true(self, url_extractor):
        ...
