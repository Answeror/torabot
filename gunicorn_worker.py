import errno
import os
import select
import socket
import gunicorn.util as util
import gunicorn.workers.sync as base
from concurrent.futures import ThreadPoolExecutor


class Worker(base.SyncWorker):

    def _handle(self, sock):
        try:
            client, addr = sock.accept()
            client.setblocking(1)
            util.close_on_exec(client)
            self.handle(sock, client, addr)

            # Keep processing clients until no one is waiting. This
            # prevents the need to select() for every client that we
            # process.

        except socket.error as e:
            if e.args[0] not in (
                errno.EAGAIN,
                errno.ECONNABORTED,
                errno.EWOULDBLOCK
            ):
                raise

    def run(self):
        with ThreadPoolExecutor(max_workers=16) as ex:
            self._run(ex)

    def _run(self, ex):
        # self.socket appears to lose its blocking status after
        # we fork in the arbiter. Reset it here.
        for s in self.sockets:
            s.setblocking(0)

        if not self.timeout:
            # if no timeout is given the worker will never wait and will
            # use the CPU for nothing. This minimal timeout prevent it.
            self.timeout = 0.5

        ready = self.sockets
        while self.alive:
            self.notify()

            # Accept a connection. If we get an error telling us
            # that no connection is waiting we fall down to the
            # select which is where we'll wait for a bit for new
            # workers to come give us some love.

            for sock in ready:
                ex.submit(self._handle, sock)

            # If our parent changed then we shut down.
            if self.ppid != os.getppid():
                self.log.info("Parent changed, shutting down: %s", self)
                return

            try:
                self.notify()
                ret = select.select(self.sockets, [], self.PIPE, self.timeout)
                if ret[0]:
                    ready = ret[0]
                    continue
            except select.error as e:
                if e.args[0] == errno.EINTR:
                    ready = self.sockets
                    continue
                if e.args[0] == errno.EBADF:
                    if self.nr < 0:
                        ready = self.sockets
                        continue
                    else:
                        return
                raise
