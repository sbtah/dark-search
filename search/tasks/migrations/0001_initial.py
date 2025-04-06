# Generated by Django 5.1.4 on 2025-04-06 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, default=None, max_length=255, unique=True)),
                ('current_celery_id', models.CharField(blank=True, max_length=100, null=True)),
                ('last_launch_date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('last_finished_date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('number_of_launches', models.IntegerField(default=0)),
                ('number_of_finished_launches', models.IntegerField(default=0)),
                ('average_time_to_finish', models.IntegerField(default=0)),
                ('importance', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('TAKEN', 'Taken'), ('FAILED', 'Failed'), ('FINISHED', 'Finished')], default='ACTIVE', max_length=10)),
                ('frequency', models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven')], default=1)),
            ],
            options={
                'verbose_name_plural': 'CrawlTasks',
                'db_table': 'crawl_tasks',
                'db_table_comment': 'Task data and statistics.',
            },
        ),
    ]
