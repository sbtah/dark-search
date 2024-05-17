from django.contrib import admin
from crawled.models import Tag, Entity, Domain, Webpage, Data


admin.site.register(Tag)
admin.site.register(Entity)
admin.site.register(Domain)
admin.site.register(Webpage)
admin.site.register(Data)
