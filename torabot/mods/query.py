def query(kind, query, timeout):
    from ..core.connection import autoccontext
    from ..core.query import query as search
    with autoccontext(commit=True) as conn:
        q = search(
            conn=conn,
            kind=kind,
            text=query,
            timeout=timeout
        )
    return q.result
