# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
    using_setuptools = True
except ImportError:
    from distutils.core import setup
    using_setuptools = False

from os.path import join, dirname

with open(join(dirname(__file__), 'engine/version.ini')) as f:
    version = f.read().strip()


setup_args = {
    'name': 'DtCrawlEngine',
    'version': version,
    'url': 'http://git.dtstack.cn/dtstack/DtCrawlEngine.git',
    'description': '一个使用http api提供爬虫脚本服务的引擎',
    'long_description': open('README.rst').read(),
    # 'author': 'Scrapy developers',
    'maintainer': 'Scrapy developers',
    'maintainer_email': ' matrixbigdata@gmail.com',
    'license': 'BSD',
    'packages': ['engine', 'engine.console'],
    'include_package_data': True,
    'package_data': {
        '': ['*.ini', '*.conf'],
    },
    'zip_safe': False,
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Internet :: WWW/HTTP',
    ],
}


if using_setuptools:
    setup_args['install_requires'] = [
        'Twisted>=8.0',
        'Scrapy>=1.0',
        'six',
        'enum-compat',
    ]
    setup_args['entry_points'] = {'console_scripts': [
        'engine = engine.console.engine_run:main'
    ]}
else:
    setup_args['scripts'] = ['engine/console/engine_run.py']

setup(**setup_args)