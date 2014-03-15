import time
from fn.iters import head, drop
from ...ut.memo import gemo
from .core import first_n_arts_safe


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
        self._gen_arts_from_head = gemo(base.gen_arts_from_head)

    def art_n(self, query, n):
        return head(drop(n, self.gen_arts_from_head(query, n + 1)))

    def gen_arts_from_head(self, query, n, return_total=None):
        yield from self._gen_arts_from_head(
            query,
            n,
            **({} if return_total is None else {'return_total': return_total})
        )
