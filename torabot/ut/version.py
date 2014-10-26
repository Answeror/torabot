import subprocess as sp


def get_version():
    '''see http://goo.gl/y6wgWV for details'''
    return sp.check_output(['git', 'describe']).decode('utf-8').strip()
