from twisted.application.service import Application
from twisted.application.internet import TimerService, TCPServer
from twisted.web import server
from twisted.python import log

from scrapy.utils.misc import load_object

from .interfaces import IEggStorage, IPoller, ISpiderScheduler, IEnvironment, IMetrics
from .eggstorage import FilesystemEggStorage
from .scheduler import SpiderScheduler
from .poller import QueuePoller
from .environ import Environment
from .metrics import MetricsReporter
from .config import Config


def application(config):
    """
    提供http服务并启动应用
    :param config:
    :return:
    """
    app = Application("engine")
    http_port = config.getint('http_port', 6800)
    bind_address = config.get('bind_address', '127.0.0.1')
    poll_interval = config.getfloat('poll_interval', 5)

    poller = QueuePoller(config)
    eggstorage = FilesystemEggStorage(config)
    scheduler = SpiderScheduler(config)
    environment = Environment(config)
    # metrics = MetricsReporter(config)

    app.setComponent(IPoller, poller)
    app.setComponent(IEggStorage, eggstorage)
    app.setComponent(ISpiderScheduler, scheduler)
    app.setComponent(IEnvironment, environment)
    # app.setComponent(IMetrics, metrics)

    laupath = config.get('launcher', 'engine.launcher.Launcher')
    laucls = load_object(laupath)
    launcher = laucls(config, app)

    webpath = config.get('webroot', 'engine.website.Root')
    webcls = load_object(webpath)

    timer = TimerService(poll_interval, poller.poll)
    webservice = TCPServer(http_port, server.Site(webcls(config, app)), interface=bind_address)
    log.msg(format="DtCrawlEngine 访问地址 at http://%(bind_address)s:%(http_port)s/",
            bind_address=bind_address, http_port=http_port)

    launcher.setServiceParent(app)
    timer.setServiceParent(app)
    webservice.setServiceParent(app)

    return app
