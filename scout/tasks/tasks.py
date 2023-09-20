from celery import shared_task


@shared_task(bind=True, ignore_result=True,)
def crawling_task(self):
    from logic.launcher.launcher import CrawlerLauncher
    # print(f'DEBUG QUEUE: {self.request.delivery_info["routing_key"]}')
    CrawlerLauncher().launch(task_id=self.request.id)


@shared_task(bind=True, ignore_result=True)
def reactivate_finished(self):
    from logic.organizers.organizer import TaskOrganizer
    TaskOrganizer().process_finished_tasks()


@shared_task(bind=True, ignore_result=True)
def reactivate_taken(self):
    from logic.organizers.organizer import TaskOrganizer
    TaskOrganizer().process_taken_tasks()
