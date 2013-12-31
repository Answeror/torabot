import os

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
CONNECTION_STRING = (
    'postgresql+psycopg2://{0}:{0}@localhost/{0}'
    .format('torabot-dev')
)

if __name__ == '__main__':
    from torabot import make
    app = make(
        connection_string=CONNECTION_STRING,
        instance_path=os.path.join(CURRENT_PATH, 'data'),
        instance_relative_config=True,
        config={
            'SECRET_KEY': 'test'
        },
    )
    app.run(debug=True)
