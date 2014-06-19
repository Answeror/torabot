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


def gunicorn():
    with settings(warn_only=True):
        kill('gunicorn')
        kill('celery')
        kill('scrapyd')
    # run('redis-cli flushall')
    run('redis-cli keys "torabot:temp:*" | xargs redis-cli del')
    run('redis-cli keys "torabot:spy:*" | xargs redis-cli del')
    with cd('/www/torabot/repo'):
        run('git pull')
        with prefix('pyenv shell 2.7.6'):
            with prefix('pyenv virtualenvwrapper'):
                with prefix('workon www27'):
                    run('pip install -r dependencies-27.txt')
                    runbg('scrapyd')
                    run('./deployspy')
        with prefix('pyenv shell 3.3.4'):
            with prefix('pyenv virtualenvwrapper'):
                with prefix('workon torabot'):
                    run('pip install -r dependencies.txt')
                    run('python setup.py develop')
                    runbg('celery worker -A torabot -f data/celery-worker.log --autoscale=4,1')
                    runbg('celery beat -A torabot -f data/celery-beat.log')
                    runbg('gunicorn --pythonpath . -t 600 -w 2 -k gunicorn_worker.Worker gunicorn_app:app')
