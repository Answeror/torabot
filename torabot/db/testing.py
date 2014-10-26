class SandboxTestSuiteMixin(object):

    def setup(self):
        from . import db
        super().setup()
        self.sandbox = db.sandbox()
        self.sandbox.__enter__()

    def teardown(self):
        self.sandbox.__exit__(None, None, None)
        super().teardown()
