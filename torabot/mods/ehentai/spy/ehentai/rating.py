def parse_rating(s):
    ps = s.split(';')
    assert len(ps) == 2
    p = ps[0]
    prefix = 'background-position:'
    assert p.startswith(prefix)
    ps = p[len(prefix):].split()
    assert len(ps) == 2
    assert all([a.endswith('px') for a in ps])
    ps = [int(a[:-len('px')]) for a in ps]
    assert ps[0] % 16 == 0
    assert ps[1] in (-1, -21)
    return float(5 + ps[0] // 16 - (0.5 if ps[1] == -21 else 0))
