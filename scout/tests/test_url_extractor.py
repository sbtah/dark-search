from logic.parsers.url import UrlExtractor


class TestUrlExtractor:

    def test_url_extractor_root_domain(self):
        """Test that root domain is properly set from starting_url."""
        extractor = UrlExtractor(starting_url='http://found.onion/')
        assert extractor.root_domain == 'found.onion'

    def test_url_extractor_parse(self, url_extractor_case_1):
        """Test UrlExtractor's parse method."""
        results = url_extractor_case_1.parse()
        assert results == {
            'internal': {'http://example.onion/page', 'http://example.onion/path'},
            'external': {'http://external.onion/'}
        }
