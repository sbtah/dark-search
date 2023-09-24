from django.contrib import admin
from crawled.models import Tag, Webpage, Domain


class WebpageAdmin(admin.ModelAdmin):

    readonly_fields = (
        'parent_domain',
        'url',
        'url_after_request',
        'last_http_status',
        'average_response_time',
        'raw_html',
        'page_title',
        'meta_title',
        'meta_description',
        'last_visit',
        'on_page_raw_urls',
        'on_page_processed_urls',
        'number_of_successful_requests',
        'number_of_unsuccessful_requests',
        'is_active',
        'created',
    )
    list_select_related = ('parent_domain', )
    list_display = (
        'url',
        'created',
        'page_title',
        'meta_title',
        'meta_description',
        'last_visit',
        'is_active',
    )
    search_fields = [
        'page_title',
        'meta_title',
        'meta_description',
    ]


class DomainAdmin(admin.ModelAdmin):
    readonly_fields = (
        'value',
        'created',
        'last_crawl_date',
        'average_crawl_time',
        'server',
        'description',
        'number_of_crawls_finished',
        'number_of_pages_found',
        'site_structure',
    )
    list_display = (
        'value',
        'created',
        'last_crawl_date',
        'average_crawl_time',
        'server',
        'description',
        'number_of_crawls_finished',
        'number_of_pages_found',
    )
    search_fields = [
        'value',
        'description',
    ]




admin.site.site_header = 'Tor Scout API'
admin.site.register(Tag)
admin.site.register(Webpage, WebpageAdmin)
admin.site.register(Domain, DomainAdmin)
