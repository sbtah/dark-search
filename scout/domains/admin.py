from django.contrib import admin
from domains.models import Domain



admin.site.site_header = 'Tor Scout'
admin.site.register(Domain)