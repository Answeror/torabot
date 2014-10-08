from logbook.compat import redirect_logging
redirect_logging()

import os


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    from torabot.core.log import RedisPub

    with RedisPub():
        from torabot import make
        app = make(
            instance_path=os.path.join(CURRENT_PATH, 'data'),
            instance_relative_config=True,
        )
        app.run(threaded=True, debug=True)
