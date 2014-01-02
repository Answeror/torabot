from torabot.notice import listen, pop_changes, pop_notices
from threading import Thread
from torabot.model import makesession, Session
from torabot.exception import exception_guard


CONNECTION_STRING = (
    'postgresql+psycopg2://{0}:{0}@localhost/{0}'
    .format('torabot-dev')
)
TIMEOUT = 5


@exception_guard
def listen_change():
    with makesession(commit=True) as session:
        action = lambda: pop_changes(session)
        if not listen('change', action, timeout=TIMEOUT):
            action()


@exception_guard
def listen_notice():
    with makesession(commit=True) as session:
        action = lambda: pop_notices(echo, session)
        if not listen('change', action, timeout=TIMEOUT):
            action()


def echo(notice, session):
    print(notice.text)
    return True


def forever(f):
    while True:
        f()


def initdb():
    from sqlalchemy import create_engine
    engine = create_engine(CONNECTION_STRING)
    Session.configure(bind=engine)


if __name__ == '__main__':
    initdb()

    change_thread = Thread(target=forever, args=(listen_change,))
    notice_thread = Thread(target=forever, args=(listen_notice,))
    change_thread.start()
    notice_thread.start()
    change_thread.join()
    notice_thread.join()
