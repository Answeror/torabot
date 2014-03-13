import os

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
TORABOT_CONNECTION_STRING = (
    'postgresql+psycopg2://{0}:{0}@localhost/{0}'
    .format('torabot-dev')
)

if __name__ == '__main__':
    from torabot import make
    app = make(
        instance_path=os.path.join(CURRENT_PATH, 'data'),
        instance_relative_config=True,
        config={
            'SECRET_KEY': 'test',
            'TORABOT_CONNECTION_STRING': TORABOT_CONNECTION_STRING,
        },
    )
    app.run(debug=True)
