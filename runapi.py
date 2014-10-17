from torabot.api import app


if __name__ == '__main__':
    server = app.make_server()
    server.start()
