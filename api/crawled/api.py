from ninja import Router
from crawled.schemas import ResponseSchema


router = Router()


@router.post('/process-response')
async def test(request, crawled_response: ResponseSchema):
    print(crawled_response.dict())
    return crawled_response
