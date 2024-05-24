from django.contrib import admin
from parameters.models import UserAgent, Proxy


admin.site.register(UserAgent)
admin.site.register(Proxy)