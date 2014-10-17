from flask import Flask, _request_ctx_stack
import inspect
import asyncio


class Alask(Flask):

    def make_response(self, rv):
        if isinstance(rv, asyncio.Future) or inspect.isgenerator(rv):
            return Response(self, rv, _request_ctx_stack.top.copy())
        return Flask.make_response(self, rv)


class Response(Flask.response_class):

    def __init__(self, app, coro_or_future, request_context):
        self.app = app
        self.coro_or_future = coro_or_future
        self.request_context = request_context

    @asyncio.coroutine
    def __call__(self, environ, start_response):
        with self.request_context:
            rv = yield from self.coro_or_future
        resp = Flask.make_response(self.app, rv)
        return resp(environ, start_response)
