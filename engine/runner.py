import sys
import os
import shutil
import tempfile
from contextlib import contextmanager

from engine import get_application
from engine.interfaces import IEggStorage
from engine.eggutils import activate_egg

@contextmanager
def project_environment(project):
    app = get_application()
    eggstorage = app.getComponent(IEggStorage)
    eggversion = os.environ.get('SCRAPY_EGG_VERSION', None)
    version, eggfile = eggstorage.get(project, eggversion)
    if eggfile:
        prefix = '%s-%s-' % (project, version)
        fd, eggpath = tempfile.mkstemp(prefix=prefix, suffix='.egg')
        lf = os.fdopen(fd, 'wb')
        shutil.copyfileobj(eggfile, lf)
        lf.close()
        activate_egg(eggpath)
    else:
        eggpath = None
    try:
        assert 'engine.conf' not in sys.modules, "Scrapy settings already loaded"
        yield
    finally:
        if eggpath:
            os.remove(eggpath)

def main():
    project = os.environ['SCRAPY_PROJECT']
    with project_environment(project):
        from scrapy.cmdline import execute
        execute()

if __name__ == '__main__':
    main()
