from celery import shared_task


@shared_task(bind=True, ignore_result=True,)
def crawling_task(self):
    from logic.launchers.launcher import CrawlerLauncher
    CrawlerLauncher().launch(task_id=self.request.id)


@shared_task(bind=True, ignore_result=True)
def reactivate_finished(self):
    from logic.organizers.organizer import TaskOrganizer
    TaskOrganizer().process_finished_tasks()


@shared_task(bind=True, ignore_result=True)
def reactivate_taken(self):
    from logic.organizers.organizer import TaskOrganizer
    TaskOrganizer().process_taken_tasks()
