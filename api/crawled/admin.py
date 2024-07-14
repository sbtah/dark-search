from django.contrib import admin
from crawled.models.tag import Tag
from crawled.models.entity import Entity
from crawled.models.domain import Domain
from crawled.models.webpage import Webpage, Data


admin.site.register(Tag)
admin.site.register(Entity)
admin.site.register(Domain)
admin.site.register(Webpage)
admin.site.register(Data)
