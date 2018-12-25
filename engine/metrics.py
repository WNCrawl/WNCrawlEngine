from zope.interface import implementer
from six import iteritems
from twisted.internet.defer import DeferredQueue, inlineCallbacks, maybeDeferred, returnValue
import time

from .utils import get_spider_queues
from .interfaces import IMetrics
import threading
import requests


@implementer(IMetrics)
class MetricsReporter(object):
    """
    metrics报告器
    """
    def __init__(self, config):
        self.config = config
        self.heart_beat()

    def _send(self, url, data):
        """
        发送数据
        :param url:
        :param data:
        :return:
        """
        while 1:
            time.sleep(30)
            try:
                requests.post(url, json=data)
            except Exception as ex:
                import traceback
                print("error = {}".format(traceback.format_exc()))

    def heart_beat(self):
        manager = self.config.items('manager', ())
        host = self.config.get("bind_address")
        port = self.config.get("http_port")
        for key, val in manager:

            data = {
                "node_name": host,
                "node_ip": host,
                "node_port": port,
                "node_description": "",
                "auth": 0,
                "username": "",
                "password": "",
                "node_type": 1
            }

            beat_runner = threading.Thread(target=self._send, args=(val, data))
            beat_runner.start()

    def report_metric(self):
        pass


