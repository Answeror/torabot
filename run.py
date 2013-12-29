CONNECTION_STRING = (
    'postgresql+psycopg2://{0}:{0}@localhost/{0}'
    .format('torabot-dev')
)

if __name__ == '__main__':
    from torabot import make
    app = make(
        connection_string=CONNECTION_STRING,
    )
    app.run(debug=True)
