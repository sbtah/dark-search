from django.contrib import admin
from crawled.models import Tag, Webpage, Website


admin.site.register(Tag)
admin.site.register(Webpage)
admin.site.register(Website)