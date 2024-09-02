import os
import threading
from enum import Enum

from prometheus_client import Counter, Gauge, Summary, Histogram

from business.common.constant import MetricKey
from ctools import call, cjson, sys_log
from ctools.application import Server

log = sys_log.flog

metrics = {}
_metrics_initial = {}
persistent_json = {}
temp_metrics_json = {}
is_metrics_init: bool = True
_lock = threading.Lock()


class MetricType(Enum):
  COUNTER = 'counter'
  GAUGE = 'gauge'
  SUMMARY = 'summary'
  HISTOGRAM = 'histogram'


class Metric:
  def __init__(self, metric_type: MetricType, metric_key: str, metric_labels: [],
               persistent: bool = False, buckets: [] = None, reset: bool = False, desc: str = ""):
    self.metric_type = metric_type
    self.metric_key = metric_key
    self.metric_labels = metric_labels
    self.buckets = buckets
    self.metric = None
    self.persistent = persistent
    self.reset = reset
    if metric_type == MetricType.COUNTER:
      self.metric = Counter(metric_key, desc, metric_labels)
    elif metric_type == MetricType.GAUGE:
      self.metric = Gauge(metric_key, desc, metric_labels)
    elif metric_type == MetricType.SUMMARY:
      self.metric = Summary(metric_key, desc, metric_labels)
    elif metric_type == MetricType.HISTOGRAM:
      if buckets is None: raise Exception('histogram buckets can not empty')
      self.metric = Histogram(metric_key, desc, metric_labels, buckets=self.buckets)
    else:
      raise Exception('metric type not found')
    _metrics_initial[metric_key] = self


@call.once
def init():
  global is_metrics_init
  global temp_metrics_json
  persistent_path = os.path.join(Server.indicatorsPath, 'persistent.json')
  if os.path.exists(persistent_path):
    with open(persistent_path, 'r') as persistent_file:
      global persistent_json
      try:
        content = persistent_file.readline()
        # log.info("persistent初始化: %s" % content)
        persistent_json = cjson.loads(content)
      except Exception:
        log.error('persistent.json is not valid json!!!!!')
        persistent_json = {}
  _init_all_metrics()
  for key, item in persistent_json.items():
    metrics_key = key.split("-")[0]
    if '_labels' in key or metrics_key not in _metrics_initial: continue
    opt(metrics_key, persistent_json[key + '_labels'], persistent_json[key])
  persistent_metrics()
  is_metrics_init = False


@call.schd(60, start_by_call=True)
def persistent_metrics():
  if persistent_json and not _lock.locked():
    with open(os.path.join(Server.indicatorsPath, 'persistent.json'), 'w') as persistent_file:
      persistent_file.write(cjson.dumps(persistent_json))
      persistent_file.flush()


def opt(metric_key: str, label_values: [], metric_value: int):
  _lock.acquire(timeout=5)
  try:
    persistent_key = "%s-%s" % (metric_key, "_".join(map(str, label_values)))
    metric_entity: Metric = metrics.get(persistent_key)
    if not metric_entity:
      metric_entity = metrics[persistent_key] = _metrics_initial[metric_key]

    if metric_entity.persistent:
      if not is_metrics_init and not metric_entity.reset and persistent_key in persistent_json:
        persistent_json[persistent_key] += metric_value
      else:
        persistent_json[persistent_key] = metric_value
      persistent_json[persistent_key + '_labels'] = label_values

      if persistent_json[persistent_key] < 0:
        persistent_json[persistent_key] = 0
        metric_value = 0

    temp_metrics_json[persistent_key] = metric_value

    if metric_entity.metric_type == MetricType.COUNTER or metric_entity.metric_type == MetricType.GAUGE:
      if label_values is None or len(label_values) == 0:
        if metric_entity.metric_type == MetricType.COUNTER and metric_entity.reset:
          metric_entity.metric.reset()
        metric_entity.metric.inc(metric_value)
      else:
        if metric_entity.reset:
          try:
            metric_entity.metric.remove(*label_values)
          except Exception:
            pass
        metric_entity.metric.labels(*label_values).inc(metric_value)
    else:
      if label_values is None or len(label_values) == 0:
        metric_entity.metric.observe(metric_value)
      else:
        metric_entity.metric.labels(*label_values).observe(metric_value)
  except Exception as e:
    log.error("添加指标信息异常: %s" % e)
  _lock.release()


def _init_all_metrics():
  Metric(MetricType.COUNTER, 'demo123123', ['asdasd', 'sdfsdf'], persistent=True)
  Metric(MetricType.GAUGE, MetricKey.ASSETS_TPL_COUNT.value, [], persistent=True, desc="模版数量")
  Metric(MetricType.GAUGE, MetricKey.ASSETS_FLOW_COUNT.value, [], persistent=True, desc="流程数量")
  Metric(MetricType.GAUGE, MetricKey.ASSETS_SCHEDULE_COUNT.value, [], persistent=True, desc="调度任务数量")

  Metric(MetricType.COUNTER, MetricKey.CLIENT_STATUS_RUNNING_STATE.value, [], reset=True, desc="运行状态")
  Metric(MetricType.COUNTER, MetricKey.CLIENT_STATUS_AUTHORIZED_DAYS.value, [], reset=True, desc="已授权天数")
  Metric(MetricType.COUNTER, MetricKey.CLIENT_STATUS_PROGRESS.value, ['process_id'], reset=True, desc="流程运行进度[0-100]")

  Metric(MetricType.COUNTER, MetricKey.WORKLOAD_PROCESS_EXEC_COUNT.value, ['process_id'], persistent=True, desc="流程执行次数")
  Metric(MetricType.COUNTER, MetricKey.WORKLOAD_PROCESS_HOURS.value, ['process_id'], persistent=True, desc="全部流程工作时长")
  Metric(MetricType.COUNTER, MetricKey.WORKLOAD_PROCESS_HOURS_SINGLE.value, ['process_id'], reset=True, desc="单次流程工作时长")
  Metric(MetricType.COUNTER, MetricKey.WORKLOAD_PROCESS_COLLECT_DATA_TOTAL.value, ['process_id'], persistent=True, desc="全部流程采集数据总量")
  Metric(MetricType.COUNTER, MetricKey.WORKLOAD_PROCESS_COLLECT_DATA_TOTAL_SINGLE.value, ['process_id'], reset=True, desc="单次流程采集数据总量")
  Metric(MetricType.COUNTER, MetricKey.WORKLOAD_PROCESS_SEND_DATA_TOTAL.value, ['process_id'], persistent=True, desc="全部流程发送数据总量")
  Metric(MetricType.COUNTER, MetricKey.WORKLOAD_PROCESS_SEND_DATA_TOTAL_SINGLE.value, ['process_id'], reset=True, desc="单次流程发送数据总量")

  Metric(MetricType.COUNTER, MetricKey.ERROR_SCHEDULE_COUNT.value, ['process_id'], persistent=True, desc="出错任务数")
