from django.contrib import admin
from tasks.models import Task



class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'type',
        'importance',
        'number_of_launches',
        'last_crawl_start',

    )
admin.site.register(Task, TaskAdmin)