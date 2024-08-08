from ninja import NinjaAPI
from crawled.api import router as crawled_router
from crawled.models.domain import Domain



api = NinjaAPI(
    title='Dark Search API',
    description='API for Dark Search Service',
    version='0.0.1',)


@api.get('/')
def home(request):
    print()
    current_num_of_domains: int = Domain.objects.count()
    output = {
        "message": "Welcome to Dark Search",
        "current_num_of_domains": current_num_of_domains,
    }
    print(output)
    return output


api.add_router("/", crawled_router)
