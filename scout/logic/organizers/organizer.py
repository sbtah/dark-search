from logic.organizers.base import BaseOrganizer


class TaskOrganizer(BaseOrganizer):
    """
    Utility for reactivating TAKEN or FINISHED Tasks.
    Compares Task objects in db with Celery tasks results.
    Reactivates FINISHED Task according to frequency.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def process_taken_tasks(self) -> None:
        """
        Some long-running Tasks can fail,
            and Task object in db will be left in status TAKEN.
        This method is simply filtering Tasks with TAKEN status,
            and compares them with all celery tasks in all queues.
        Tasks that are not found in celery pipeline,
            are marked as ACTIVE again.
        """

        taken_tasks = self.task_adapter.get_taken_tasks()
        celery_tasks = self.get_celery_tasks()

        for task in taken_tasks:
            if task.task_id is None:
                task_obj = self.task_adapter.mark_task_active(task_object=task)
                self.logger.info(f'Marking Task as ACTIVE: {task_obj.owner.value}')
            elif task.task_id not in celery_tasks:
                task_obj = self.task_adapter.mark_task_active(task_object=task)
                self.logger.info(f'Marking Task as ACTIVE: {task_obj.owner.value}')
            else:
                # self.logger.info(f'Found Task in pipeline.: {task.owner.value}')
                continue

    def process_finished_tasks(self) -> None:
        """
        Changes Task status to ACTIVE after period of time, set as frequency.
        """

        finished_tasks = self.task_adapter.get_finished_tasks()

        for task in finished_tasks:
            task_finished_launched_date = self.generate_date_from_timestamp(
                timestamp=task.last_finished_launch_date
            )
            time_delta_frequency = self.generate_timedelta_day(
                task_frequency=task.frequency
            )
            current_date = self.generate_date_from_timestamp(
                self.generate_current_timestamp()
            )
            if current_date > (task_finished_launched_date + time_delta_frequency):
                self.task_adapter.mark_task_active(task_object=task)
                self.logger.info(
                    (f'Marking FINISHED Task as ACTIVE: {task.owner.value}')
                )

    def get_celery_tasks(self) -> set:
        """
        Fetch all celery tasks IDs in all queues.
        Return set of current celery tasks IDs.
        """

        inspect_object = self.start_inspect()
        queues = self.get_all_queues(inspect=inspect_object)
        tasks_ids = set()

        for q in queues:
            active_tasks = self._get_active_tasks(
                inspect=inspect_object,
                queue_name=q,
            )
            registered_tasks = self._get_registered_tasks(
                inspect=inspect_object,
                queue_name=q,
            )
            scheduled_tasks = self._get_scheduled_tasks(
                inspect=inspect_object,
                queue_name=q,
            )
            for at in active_tasks:
                if isinstance(at, dict):
                    if at.get('id') is not None:
                        tasks_ids.add(at.get('id'))
            for rt in registered_tasks:
                if isinstance(rt, dict):
                    if rt.get('id') is not None:
                        tasks_ids.add(rt.get('id'))
            for st in scheduled_tasks:
                if isinstance(st, dict):
                    if st.get('id') is not None:
                        tasks_ids.add(st.get('id'))
        return tasks_ids

    
    def get_all_queues(self, inspect):
        """
        Returns list of current celery queues.
        """
        queues = inspect.active_queues()
        current_queues = list(queues.keys())
        return current_queues
    
    def _get_active_tasks(self, inspect, queue_name):
        """
        Returns active celery tasks for specified queue.
        """
        active = inspect.active()
        return active[queue_name]
    
    def _get_registered_tasks(self, inspect, queue_name):
        """
        Returns registered celery tasks for specified queue.
        """
        registered = inspect.registered()
        return registered[queue_name]
    
    def _get_scheduled_tasks(self, inspect, queue_name):
        """
        Returns scheduled celery tasks for specified queue.
        """
        scheduled = inspect.scheduled()
        return scheduled[queue_name]
