from ninja import Router
from logic.schemas.response import ResponseSchema, SummarySchema


router = Router()


@router.post('/process-response')
def test(request, crawled_response: ResponseSchema):
    print(crawled_response.dict())
    return crawled_response


@router.post('/process-summary')
def test(request, crawl_summary: SummarySchema):
    # print(crawl_summary.dict())
    return crawl_summary
