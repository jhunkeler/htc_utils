import os
import subprocess
from collections import OrderedDict
from distutils.spawn import find_executable

__all__ = ['htcondor_path', 'recast', 'Job', 'Submit', 'Wait']

def htcondor_path(path=None):
    needles = ['condor_master', 'condor_submit', 'condor_wait']
    paths = []

    if path is not None:
        os.environ['PATH'] = ':'.join([os.path.join(path, 'bin'), os.environ['PATH']])
        os.environ['PATH'] = ':'.join([os.path.join(path, 'sbin'), os.environ['PATH']])

    for needle in needles:
        try:
            executable = find_executable(needle, os.environ['PATH'])
            path = os.path.dirname(executable)
            paths.append(path)
        except AttributeError:
            pass

    if not paths:
        raise OSError('Unable to find a valid HTCondor installation.')

    return ':'.join(paths)


def recast(value):
    ''' Convert value to string
    '''
    if type(value) is bool and value == True:
        value = 'true'
        return value

    if type(value) is bool and value == False:
        value = 'false'
        return value

    if isinstance(value, list) or \
        isinstance(value, tuple):
            values = ' '.join([ str(x) for x in value ])
            return values

    if isinstance(value, dict):
        temp = []
        for key, val in value.items():
            val = str(val)
            temp.append('='.join([str(key), str(val)]))
        # Ad-hoc string quoting
        return ';'.join(str(x) for x in temp)


    try:
        value = str(value)
    except:
        raise TypeError('Unable to cast "{}" to str'.format(type(value)))

    return value



from .job import *
from .submit import *
from .wait import *
