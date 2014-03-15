#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fabric.api import run, env, cd, prefix, settings


# the user to use for the remote commands
env.user = 'answeror'
# the servers where the commands are executed
env.hosts = ['aip.io']


def runbg(cmd, sockname="dtach"):
    return run('dtach -n `mktemp -u /tmp/%s.XXXX` %s' % (sockname, cmd))


def kill(name):
    run("ps auxww | grep %s | grep -v \"grep\" | awk '{print $2}' | xargs kill -9 >& /dev/null" % name)
    #run('killall %s' % name)


def gunicorn():
    with settings(warn_only=True):
        kill('celery')
        kill('gunicorn')
    with cd('/www/torabot/repo'):
        run('git pull')
        with prefix('pyenv virtualenvwrapper'):
            with prefix('workon torabot'):
                run('pip install -r dependencies.txt')
                runbg('celery worker -A torabot -f data/celery.log --autoscale=4,1')
                runbg('celery beat -A torabot')
                runbg('gunicorn --pythonpath . -t 600 -w 2 -k gunicorn_worker.Worker gunicorn_app:app')
