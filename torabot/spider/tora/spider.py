import time
from fn.iters import head, drop, take
from ...ut.memo import memo
from .core import first_n_arts_safe, ROOM


class MemorySafeSpider(object):

    def art_n(self, query, n):
        return head(drop(n, self.gen_arts_from_head(query, n + 1)))

    def gen_arts_from_head(self, query, n, return_total=False):
        from ...ut.rq import q
        job = q.enqueue(
            first_n_arts_safe,
            query,
            n,
            return_total,
        )
        count = 0
        ok = True
        while job.result is None:
            time.sleep(0.1)
            count += 1
            if count == 1000:
                ok = False
                break
        if ok:
            yield from job.result
        else:
            if return_total:
                yield 0
            yield from []


class FrozenSpider(object):

    def __init__(self, base=None):
        if base is None:
            base = MemorySafeSpider()
        self.base = base
        self._gen_arts_from_head = memo(lambda *args, **kargs: list(base.gen_arts_from_head(*args, **kargs)))

    def art_n(self, query, n):
        return head(drop(n + 1, self.gen_arts_from_head(
            query,
            max(ROOM, n + 1),
            True,
        )))

    def gen_arts_from_head(self, query, n, return_total=False):
        arts = take(n, list(self._gen_arts_from_head(
            query,
            max(ROOM, n),
            True,
        )))
        if return_total:
            yield from arts
        else:
            yield from drop(1, arts)
