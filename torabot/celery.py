from celery import Celery


app = Celery('torabot')

try:
    import toraconf
    assert toraconf
    app.config_from_object('toraconf')
except:
    app.config_from_object('torabot.conf')


from torabot import task


@app.task
def sync_all():
    task.sync_all(app.conf)


@app.task
def notice_all():
    task.notice_all(app.conf)


if __name__ == '__main__':
    app.start()
