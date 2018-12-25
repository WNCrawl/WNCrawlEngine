import pkgutil
import time
import requests
import threading
from scrapy.utils.misc import load_object
from engine.config import Config

__version__ = pkgutil.get_data(__package__, 'version.ini').decode('ascii').strip()
# __version__ = '1.2.2'
version_info = tuple(__version__.split('.')[:3])


def get_application(config=None):
    if config is None:
        config = Config()
    apppath = config.get('application', 'engine.app.application')
    appfunc = load_object(apppath)
    # heart_beat(config)
    return appfunc(config)


def send(url, data):
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


def heart_beat(cfg):
    manager = cfg.items('manager', ())
    host = cfg.get("bind_address")
    port = cfg.get("http_port")
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

        beat_runner = threading.Thread(target=send, args=(val, data))
        beat_runner.start()

