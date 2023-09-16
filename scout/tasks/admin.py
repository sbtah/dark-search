from django.contrib import admin
from tasks.models import Task



class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'type',
        'status',
        'importance',
        'average_time_to_crawl',
        'last_run',
    )
    list_filter = (
        'type',
        'status',
        'importance',
        'last_run'
    )

admin.site.register(Task, TaskAdmin)