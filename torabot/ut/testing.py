from nose.tools import nottest


@nottest
def app_test_suite(app):
    class AppTestSuite(object):

        def setup(self):
            self.ctx = app.app_context()
            self.ctx.push()

        def teardown(self):
            self.ctx.pop()

    return AppTestSuite
