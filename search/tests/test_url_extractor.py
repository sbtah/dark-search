"""
Test cases for UrlExtractor functionality.
"""
from unittest.mock import MagicMock
from urllib.parse import SplitResult

from logic.parsers.url import UrlExtractor


class TestUrlExtractor:

    def test_url_extractor_root_domain(self):
        """Test that root domain is properly set from starting_url."""
        extractor = UrlExtractor(starting_url='http://found.onion/')
        assert extractor.root_domain == 'found.onion'

    def test_url_extractor_parse(self, url_extractor, urls_collection, mocker):
        """Test UrlExtractor's parse method."""
        mocked_clear = mocker.patch(
            'logic.parsers.url.UrlExtractor.clear_parse_results', autospec=True, return_value=True
        )
        results = url_extractor.parse(urls_collection)
        mocked_clear.assert_called()
        mocked_clear.assert_called_once()
        assert mocked_clear.return_value == True
        assert results == {
            'internal': {'http://example.onion/page.html', 'http://example.onion/page', 'http://example.onion/path'},
            'external': {'external.onion'},
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
        test_url = 'http://example.onion/p=1?v=basic'
        url_extractor.current_url_split_result = MagicMock(
            spec=SplitResult, scheme='https', netloc='example.onion', path='/p=1', query='v=basic', fragment=''
        )
        assert url_extractor.clean_url(test_url) == 'http://example.onion/p=1'

    def test_clear_parse_result(self, url_extractor):
        """Test UrlExtractor's clean_parse_results method."""
        url_extractor.parse_results = {
            'internal': {'http://example.onion/page.html', 'http://example.onion/page', 'http://example.onion/path'},
            'external': {'external.onion'},
        }
        url_extractor.clear_parse_results()
        assert url_extractor.parse_results == {
            'internal': set(),
            'external': set(),
        }