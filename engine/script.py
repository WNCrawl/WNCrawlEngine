"""This module can be used to execute Scrapyd from a Scrapy command"""

import sys
import os
from cStringIO import StringIO

from twisted.python import log
from twisted.internet import reactor
from twisted.application import app

from scrapy.utils.project import project_data_dir
from scrapy.exceptions import NotConfigured

from engine import get_application
from engine.config import Config


def _get_config():
    datadir = os.path.join(project_data_dir(), 'engine')
    conf = {
        'eggs_dir': os.path.join(datadir, 'eggs'),
        'logs_dir': os.path.join(datadir, 'logs'),
        'items_dir': os.path.join(datadir, 'items'),
        'dbs_dir': os.path.join(datadir, 'dbs'),
    }
    for k in ['eggs_dir', 'logs_dir', 'items_dir', 'dbs_dir']: # create dirs
        d = conf[k]
        if not os.path.exists(d):
            os.makedirs(d)
    engine_conf = """
                    [engine]
                    eggs_dir = %(eggs_dir)s
                    logs_dir = %(logs_dir)s
                    items_dir = %(items_dir)s
                    dbs_dir  = %(dbs_dir)s
                    """ % conf
    return Config(extra_sources=[StringIO(engine_conf)])


def execute():
    try:
        config = _get_config()
    except NotConfigured:
        config = None
    log.startLogging(sys.stderr)
    application = get_application(config)
    app.startApplication(application, False)
    reactor.run()
