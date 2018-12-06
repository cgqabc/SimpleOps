#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from celery import shared_task

@shared_task
def add(x,y):
    return x+y

@shared_task
def xsum(n):
    return sum(n)



###########重写task类，实现task_id自定义输出Task ID look like: project.tasks.add-15073315189870
import time

from celery import Task

class NamedTask(Task):
    # id_gen = lambda: int(time.time() * 1000)
    id_gen = int(time.time() * 1000)


    def _gen_task_id(self):
        return {
            'task_id': '%s-%s' % (
                self.name,
                self.id_gen)}

    def apply(self, *args, **kwargs):
        kwargs.update(self._gen_task_id())
        return Task.apply(self, *args, **kwargs)

    def apply_async(self, *args, **kwargs):
        kwargs.update(self._gen_task_id())
        return Task.apply_async(self, *args, **kwargs)



@shared_task(base=NamedTask)
def add_name_id(x, y):
    return x + y