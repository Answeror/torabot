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
    from torabot import task
    task.sync_all(app.conf)


@app.task
def sync_one(query):
    from torabot import task
    task.sync_one(query, app.conf)


@app.task
def notice_all():
    from torabot import task
    task.notice_all(app.conf)


if __name__ == '__main__':
    app.start()
