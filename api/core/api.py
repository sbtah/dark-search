from ninja import NinjaAPI
from crawled.api import router as crawled_router
from crawled.models.webpage import Webpage
from logic.adapters.domain import DomainAdapter
from logic.adapters.webpage import WebpageAdapter


api = NinjaAPI(
    title='Dark Search API',
    description='API for Dark Search Service',
    version='0.0.1',)


@api.get('/')
def home(request):

    # Get Domains statistics to show.
    domain_adapter: DomainAdapter = DomainAdapter()
    current_num_of_domains: int = domain_adapter.get_number_of_known_domains()
    current_num_of_crawled_domains: int = domain_adapter.get_number_of_crawled_domains()

    # Get Webpage statistics.
    webpage_adapter: WebpageAdapter = WebpageAdapter()
    current_num_of_webpages: int = webpage_adapter.get_number_of_known_webpages()

    output = {
        "current_num_of_domains": current_num_of_domains,
        "current_num_of_crawled_domains": current_num_of_crawled_domains,
        "current_num_of_webpages": current_num_of_webpages,
    }
    return output


api.add_router("/", crawled_router)
