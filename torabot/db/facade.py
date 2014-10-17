from flask import current_app, _app_ctx_stack as stack


class Facade(object):

    def init_app(self, app):
        app.config.setdefault(
            'TORABOT_TEST_CONNECTION_STRING',
            'postgresql+psycopg2://localhost/torabot-test'
        )

    def make_engine(self):
        from sqlalchemy import create_engine
        return create_engine(
            current_app.config['TORABOT_TEST_CONNECTION_STRING']
        )

    @property
    def engine(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'engine'):
                ctx.engine = self.make_engine()
            return ctx.engine
