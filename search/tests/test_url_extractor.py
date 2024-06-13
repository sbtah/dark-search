"""
Test cases for UrlExtractor functionality.
"""
from unittest.mock import MagicMock
from urllib.parse import SplitResult

import pytest
from logic.parsers.objects.url import Url
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
        # print(results)
        assert results == {
            'internal': {
                Url(value='http://example.onion/page', anchor='Url 1', number_of_requests=0),
                Url(value='http://example.onion/path?page=1', anchor='Url 2', number_of_requests=0),
                Url(value='http://example.onion/path?query=string', anchor='Url 3', number_of_requests=0),
                Url(value='http://example.onion/path', anchor='Url 4', number_of_requests=0),
                Url(value='http://example.onion/page.html', anchor='...', number_of_requests=0),
                Url(value='http://example.onion/path', anchor='Test text', number_of_requests=0),
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
        test_split_result = MagicMock(
            spec=SplitResult, scheme='http', netloc='example.onion', path='/invalid.onion', query='', fragment=''
        )
        assert url_extractor.is_valid_url(test_split_result) is True

    def test_url_extractor_is_valid_url_returns_false(self, url_extractor):
        """Test UrlExtractor's is_valid_url method is returning False."""
        test_split_result = MagicMock(
            spec=SplitResult, scheme='', netloc='', path='/example.onion', query='', fragment=''
        )
        assert url_extractor.is_valid_url(test_split_result) is False
    #
    @pytest.mark.parametrize(
        'input, expected',
        [
            ('/example-path', True),
            ('example-path', True),
        ]
    )
    def test_url_extractor_is_path_returns_true(self, url_extractor, input, expected):
        """Test that UrlExtractor's is_path method is returning True."""
        assert url_extractor.is_path(input) is expected

    @pytest.mark.parametrize(
        'input, expected',
        [
            ('/', False),
            ('', False),
            (' ', False),
        ]
    )
    def test_url_extractor_is_path_returns_false(self, url_extractor, input, expected):
        """Test that UrlExtractor's is_path method is returning False."""
        assert url_extractor.is_path(input) is expected

    def test_url_extractor_is_onion_returns_true(self, url_extractor):
        """Test that UrlExtractor's is_onion method is returning True for onion domains."""
        test_netloc = 'example.onion'
        assert url_extractor.is_onion(test_netloc) is True


    @pytest.mark.parametrize(
        'input, expected',
        [
            ('example.com', False),
            ('example.org', False),
            ('example.edu', False),
            ('example.gov', False),
            ('example.int', False),
        ]
    )
    def test_url_extractor_is_onion_returns_false(self, url_extractor, input, expected):
        """Test that UrlExtractor's is_onion method is returning False for other than onion domains."""
        assert url_extractor.is_onion(input) is expected


    @pytest.mark.parametrize(
        'input, expected',
        [
            ('/file.zip', True), ('/file.7z', True), ('/file.rar', True), ('/file.doc', True), ('/file.docx', True),
            ('/file.docm', True),('/file.pdf', True), ('/file.ods', True), ('/file.xlsx', True), ('/file.xls', True),
            ('/file.txt', True), ('/file.odt', True), ('/file.ods', True), ('/file.tgz', True), ('/file.tar.xz', True),
            ('/file.tar.Z', True), ('/file.tar.zst', True), ('/file.tar.gz', True), ('/file.tar.lz', True),('/file.tar.bz2', True),
            ('/file.tar', True), ('/file.tlz', True), ('/file.tbz2', True), ('/file.txz', True),('/file.png', True),
            ('/file.jpg', True), ('/file.jpeg', True), ('/file.csv', True), ('/file.bin', True), ('/file.bat', True),
            ('/file.accdb', True), ('/file.dll', True), ('/file.exe', True), ('/file.gif', True), ('/file.mov', True),
            ('/file.mp3', True), ('/file.mp4', True), ('/file.mpeg', True), ('/file.mpg', True), ('/file.ppt', True),
            ('/file.pptx', True), ('/file.xps', True),
        ]
    )
    def test_url_extractor_is_file_returns_true_for_known_file_extensions(self, url_extractor, input, expected):
        """Test that UrlExtractor's is_file method is returning True for each tested path.

        """
        assert url_extractor.is_file(input) is expected

    @pytest.mark.parametrize(
        'input, expected',
        [
            ('http', True),
            ('https', True),
        ]
    )
    def test_url_extractor_is_accepted_scheme_returns_true(self, url_extractor, input, expected):
        """Test that UrlExtractor's is_accepted_scheme method is returning True."""
        assert url_extractor.is_accepted_scheme(input) is expected

    @pytest.mark.parametrize(
        'input, expected',
        [
            ('mailto', False),
            ('javascript', False),
            ('file', False),
            ('irc', False),
            ('telnet', False),

        ]
    )
    def test_url_extractor_is_accepted_scheme_returns_false(self, url_extractor, input, expected):
        """Test that UrlExtractor's is_accepted_scheme method is returning False."""
        assert url_extractor.is_accepted_scheme(input) is expected

    def test_url_extractor_clean_url(self, url_extractor):
        """Test UrlExtractor's clean_url method."""
        test_url = 'http://example.onion/path?query=string#fragment'
        assert url_extractor.clean_url(test_url) == 'http://example.onion/path?query=string'
