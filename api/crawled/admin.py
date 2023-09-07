from django.contrib import admin
from crawled.models import Tag, Webpage, Website


class WebpageAdmin(admin.ModelAdmin):

    readonly_fields = (
        'parent_website',
        'url',
        'url_after_request',
        'last_http_status',
        'average_response_time',
        'title',
        'meta_description',
        'is_file',
        'last_visit',
        'on_page_onion_urls',
        'number_of_successful_requests',
        'number_of_unsuccessful_requests',
        'is_active',
        'number_of_references',
        'created',
    )
    list_select_related = ('parent_website', )
    list_display = (
        'url',
        'created',
        'title',
        'meta_description',
        'is_file',
        'last_visit',
        'is_active',
    )


admin.site.site_header = 'Tor Scout'
admin.site.register(Tag)
admin.site.register(Webpage, WebpageAdmin)
admin.site.register(Website)
