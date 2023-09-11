from django.contrib import admin
from crawled.models import Tag, Webpage, Domain


class WebpageAdmin(admin.ModelAdmin):

    readonly_fields = (
        'parent_domain',
        'url',
        'url_after_request',
        'last_http_status',
        'average_response_time',
        'title',
        'meta_description',
        'last_visit',
        'on_page_raw_urls',
        'on_page_processed_urls',
        'number_of_successful_requests',
        'number_of_unsuccessful_requests',
        'is_active',
        'number_of_references',
        'created',
    )
    list_select_related = ('parent_domain', )
    list_display = (
        'url',
        'created',
        'title',
        'meta_description',
        'last_visit',
        'is_active',
    )
    list_filter = (
        'parent_domain',
    )


class DomainAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'url',
        'title',
        'description',
        'created',
        'last_crawl',
        'server',
    )



admin.site.site_header = 'Tor Scout API'
admin.site.register(Tag)
admin.site.register(Webpage, WebpageAdmin)
admin.site.register(Domain, DomainAdmin)
