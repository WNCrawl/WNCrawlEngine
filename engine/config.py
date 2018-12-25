import glob
from io import StringIO
from pkgutil import get_data
from six.moves.configparser import SafeConfigParser, NoSectionError, NoOptionError
from os.path import expanduser

from scrapy.utils.conf import closest_scrapy_cfg


class Config(object):
    """
    配置文件解析功能的一个简单包装
    A ConfigParser wrapper to support defaults when calling instance
    methods, and also tied to a single section
    """

    SECTION = 'engine'

    def __init__(self, values=None, extra_sources=()):
        if values is None:
            sources = self._getsources()
            default_config = get_data(__package__, 'default_engine.conf').decode('utf8')
            self.cp = SafeConfigParser()
            self.cp.readfp(StringIO(default_config))
            self.cp.read(sources)
            for fp in extra_sources:
                self.cp.readfp(fp)
        else:
            self.cp = SafeConfigParser(values)
            self.cp.add_section(self.SECTION)

    def _getsources(self):
        """
        获取配置文件
        :return:
        """
        sources = ['/etc/engine/engine.conf', r'c:\engine\engine.conf']
        sources += sorted(glob.glob('/etc/engine/conf.d/*'))
        sources += ['engine.conf']
        sources += [expanduser('~/.engine.conf')]
        scrapy_cfg = closest_scrapy_cfg()
        if scrapy_cfg:
            sources.append(scrapy_cfg)
        return sources

    def _getany(self, method, option, default):
        try:
            return method(self.SECTION, option)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise

    def get(self, option, default=None):
        return self._getany(self.cp.get, option, default)

    def getint(self, option, default=None):
        return self._getany(self.cp.getint, option, default)

    def getfloat(self, option, default=None):
        return self._getany(self.cp.getfloat, option, default)

    def getboolean(self, option, default=None):
        return self._getany(self.cp.getboolean, option, default)

    def items(self, section, default=None):
        try:
            return self.cp.items(section)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise
