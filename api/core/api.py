from ninja import NinjaAPI
from crawled.api import router as crawled_router


api = NinjaAPI(
    title='Dark Search API',
    description='API for Dark Search Service',
    version='0.0.1',)


@api.get('/')
async def home(request):
    return {"message": "Hello World"}


api.add_router("/", crawled_router)
