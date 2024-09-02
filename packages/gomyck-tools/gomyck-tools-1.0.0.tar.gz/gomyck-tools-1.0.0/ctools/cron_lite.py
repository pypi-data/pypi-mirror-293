#!/usr/bin/env python3.6
# coding: utf-8
import sched
import threading
import time
import traceback
from datetime import datetime
from functools import wraps
from typing import Optional, Dict

import pytz
from croniter import croniter


class SchedulerMeta:
  timer_task_name: str = None
  switch: bool = True
  status: bool = False
  event: sched.Event = None
  scheduler: sched.scheduler = None


scheduler_map: Dict[str, SchedulerMeta] = {}  # {timer_task_name: SchedulerMeta}
_switch = False
_error_handler = print
_info_handler = print
_time_zone: Optional[pytz.BaseTzInfo] = None


def set_time_zone(time_zone_name: str):
  global _time_zone
  _time_zone = pytz.timezone(time_zone_name)


def _register_next(timer_task_name, base_func, cron_expr, till_time_stamp):
  cron_obj = croniter(cron_expr)
  if _time_zone:
    cron_obj.set_current(datetime.now(tz=_time_zone))
  next_time = int(cron_obj.get_next())
  if scheduler_map.get(timer_task_name) is None:
    scheduler_meta = SchedulerMeta()
    scheduler_meta.timer_task_name = timer_task_name
    scheduler_meta.switch = True
    scheduler_meta.scheduler = sched.scheduler(time.time, time.sleep)
    scheduler_map[timer_task_name] = scheduler_meta
  if till_time_stamp is None or next_time <= till_time_stamp:
    scheduler_map[timer_task_name].event = scheduler_map[timer_task_name].scheduler.enterabs(next_time, 0, base_func)


def _run_sched(scheduler_meta: SchedulerMeta):
  active(scheduler_meta.timer_task_name)
  while True:
    scheduler = scheduler_meta.scheduler
    if not _switch or not scheduler_meta.switch:
      scheduler.empty()
      inactive(scheduler_meta.timer_task_name)
      return
    t = scheduler.run(False)
    if t is None:
      inactive(scheduler_meta.timer_task_name)
      return
    st = time.time()
    while time.time() - st < t:
      if not _switch or not scheduler_meta.switch:
        scheduler.empty()
        inactive(scheduler_meta.timer_task_name)
        return
      time.sleep(0.5)


def _start():
  global _switch
  _info_handler("cron started")
  tl = []
  for timer_task_name, scheduler_meta in scheduler_map.items():
    print("Registering Job:", timer_task_name)
    t = threading.Thread(target=_run_sched, args=(scheduler_meta,), daemon=True)
    # 有些task非常耗时，会影响退出。目前设计改为退出时不保证task完成
    t.start()
    tl.append(t)

  for t in tl:
    t.join()
  _info_handler("cron finished")
  _switch = False  # ensure close when there are no more tasks with switch open
  scheduler_map.clear()


def convert_cron(cron_expr):
  res_cron = ""
  cron_list = cron_expr.split(" ")
  if len(cron_list) > 6:
    for cron in cron_list[1:]:
      if cron != "?":
        res_cron += "%s " % cron
    res_cron += "%s" % cron_list[0]
  else:
    res_cron = cron_expr
  return res_cron


def cron_task(cron_expr: str, till_time_stamp: int = None):
  """
  cron_task decorator to register a function as crontab task
  :param cron_expr: the croniter accepted cron_expression. NOTICE: the default timezone is UTC and can be changed by
  `set_time_zone`. The format is `min hour day month weekday [sec]`
  :param till_time_stamp: run this jog till when. None means forever
  :return: the real decorator
  """
  cron_expr = convert_cron(cron_expr)
  assert len(cron_expr.split(" ")) in (5, 6), \
    "only supported <min hour day month weekday> and <min hour day month weekday sec>"

  def deco(func):
    @wraps(func)
    def inner():
      try:
        func()
      except Exception:
        try:
          _error_handler(f"run {func.__name__} failed\n" + traceback.format_exc())
        except Exception:
          _error_handler(f"run {func.__name__} failed\n")
      _register_next(inner, inner, cron_expr, till_time_stamp)

    _register_next(inner, inner, cron_expr, till_time_stamp)
    return inner

  return deco


def apply_cron_task(timer_task_name, func, params, cron_expr, till_time_stamp=None):
  """
  cron_task decorator to register a function as crontab task
  :param func: task callback function
  :param params: transparent parameters
  :param cron_expr: the croniter accepted cron_expression. NOTICE: the default timezone is UTC and can be changed by
  `set_time_zone`. The format is `min hour day month weekday [sec]`
  :param timer_task_name: task name
  :param till_time_stamp: run this jog till when. None means forever
  :return: the real decorator
  """
  cron_expr = convert_cron(cron_expr)
  assert len(cron_expr.split(" ")) in (5, 6), \
    "Only supported <minute hour day month weekday> and <minute hour day month weekday second>"

  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      func(timer_task_name, params, *args, **kwargs)
    except Exception as exc:
      _error_handler(f"Run {func.__name__} failed with error: {str(exc)}")
    finally:
      _register_next(timer_task_name, wrapper, cron_expr, till_time_stamp)

  _register_next(timer_task_name, wrapper, cron_expr, till_time_stamp)

  global _switch
  _switch = True

  scheduler = scheduler_map.get(timer_task_name)
  if scheduler:
    scheduler.switch = True
    t = threading.Thread(target=_run_sched, name=timer_task_name, args=(scheduler,), daemon=True)
    # 有些task非常耗时，会影响退出。目前设计改为退出时不保证task完成
    t.start()
  return wrapper


def start_all(spawn: bool = True, info_handler=None, error_handler=None) -> Optional[threading.Thread]:
  """
  start_all starts all cron tasks registered before.
  :param spawn: whether to start a new thread for scheduler. If not, the action will block the current thread
  :param info_handler: handle info output (scheduler start / stop), default = print, can use logging.info
  :param error_handler: handle error output (task execute exception), default = print, can use logging.error
  :raise RuntimeError: if the tasks are already started and still running we cannot start again. The feature is not
  concurrent-safe
  :return: the new thread if spawn = True
  """
  global _switch, _info_handler, _error_handler
  if _switch:
    raise RuntimeError("the crontab was already started")
  if info_handler:
    _info_handler = info_handler
  if error_handler:
    _error_handler = error_handler

  _switch = True
  if spawn:
    t = threading.Thread(target=_start)
    t.setDaemon(True)
    t.start()
    return t
  else:
    _start()


def is_active(timer_task_name):
  res = False
  if timer_task_name in scheduler_map:
    res = scheduler_map.get(timer_task_name).switch or scheduler_map.get(timer_task_name).status
  return res


def active(timer_task_name):
  if timer_task_name in scheduler_map:
    scheduler_map.get(timer_task_name).status = True

def get_switch(timer_task_name):
  switch = True
  if timer_task_name in scheduler_map:
    switch = scheduler_map.get(timer_task_name).switch
  return switch


def inactive(timer_task_name):
  if timer_task_name in scheduler_map:
    scheduler_map.get(timer_task_name).status = False
    if not scheduler_map.get(timer_task_name).switch:
      scheduler_map.get(timer_task_name).scheduler.cancel(scheduler_map[timer_task_name].event)


def stop(timer_task_name):
  if timer_task_name in scheduler_map:
    scheduler_map.get(timer_task_name).switch = False
    time.sleep(1)


def stop_all(wait_thread: Optional[threading.Thread] = None):
  """
  stop_all turns off the switch to stop the scheduler. Running jobs will be wait till finished.
  :param wait_thread: join() the spawned scheduler thread (if you started it as spawn and you want) to ensure all jobs
  to finish
  :return:
  """
  for timer_task_name in scheduler_map:
    scheduler_map.get(timer_task_name).switch = False
  if wait_thread:
    wait_thread.join()
