from celery import Celery


app = Celery('torabot')

try:
    import toraconf
    assert toraconf
    app.config_from_object('toraconf')
except:
    app.config_from_object('torabot.conf')


@app.task
def sync_all():
    from torabot import tasks
    tasks.sync_all(app.conf)


@app.task
def notice_all():
    from torabot import tasks
    tasks.notice_all(app.conf)


@app.task
def log_to_file():
    from torabot import tasks
    tasks.log_to_file()


if __name__ == '__main__':
    app.start()
