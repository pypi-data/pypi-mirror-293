from curvesimplify.agarwal import min_err


def test_min_err(vert):
    assert len(min_err(vert, 2)[0]) == 2
