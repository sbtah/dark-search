from django.contrib import admin
from tasks.models import Task



class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'type',
        'status',
        'frequency',
        'importance',
        'number_of_launches',
        'number_of_finished_launches',
        'last_launch_date',
        'last_finished_launch_date',
        'average_time_to_crawl',
        'task_id',
    )


admin.site.register(Task, TaskAdmin)