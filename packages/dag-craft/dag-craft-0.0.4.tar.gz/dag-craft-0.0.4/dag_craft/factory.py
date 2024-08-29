from typing import List
from airflow.utils.types import NOTSET, ArgNotSet
from datetime import datetime
from dag_craft.models.task import TaskModel
import logging
from airflow.decorators import dag
from typing import Union
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from airflow.utils.task_group import TaskGroup

ScheduleInterval = Union[None, str, timedelta, relativedelta]


class DagFactory:
    def __init__(
        self,
        dag_id: str,
        tasks: List[TaskModel],
        schedule_interval: Union[ArgNotSet, ScheduleInterval] = NOTSET,
        start_date: datetime | None = None,
        catchup: bool = False,
        description: str | None = None,
    ):
        self.dag_id = dag_id
        self.tasks = tasks
        self.schedule_interval = schedule_interval
        self.start_date = start_date
        self.catchup = catchup
        self.description = description

    def create_dag(self):
        task_dict = {}
        task_groups = {}

        for task in self.tasks:
            if task.task_group:
                if task.task_group not in task_groups:
                    task_groups[task.task_group] = TaskGroup(group_id=task.task_group)
                with task_groups[task.task_group]:
                    task_obj = task.operator(task_id=task.task_id, **task.operator_args)
            else:
                task_obj = task.operator(task_id=task.task_id, **task.operator_args)
            task_dict[task.task_id] = task_obj

        for task in self.tasks:
            if task.dependencies:
                for dep in task.dependencies:
                    task_dict[dep] >> task_dict[task.task_id]

        return task_dict.values()

    def register_dag(self):
        @dag(
            dag_id=self.dag_id,
            schedule_interval=self.schedule_interval,
            start_date=self.start_date,
            catchup=self.catchup,
            description=self.description,
        )
        def generated_dag():
            return self.create_dag()

        generated_dag()
