# -*- coding: utf-8 -*-
'''laporte_journal app version and resources info'''

from platform import python_version
import pkg_resources

__version__ = '0.0.1'


def get_build_info():
    '''get app version and resources info'''
    ret = {
        'laporte-journal':
        __version__,
        'python':
        python_version(),
        'python-socketio':
        pkg_resources.get_distribution("python-socketio").version,
        'python-engineio':
        pkg_resources.get_distribution("python-engineio").version
    }
    return ret
