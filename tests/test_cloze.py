from cloze.questions import ClozeQuestion


def test_example1_1():
    q = ClozeQuestion("This has answer 17 with 0 tolerance: {2:NM:~%100%17:0}")
    assert q.solve([17]) == 2.0


def test_example1_2():
    q = ClozeQuestion("This has answer 17 with 0 tolerance: {2:NM:~%100%17:0}")
    assert q.solve([3]) == 0


def test_example2_1():
    q = ClozeQuestion("{1:NUMERICAL:~%100%2:0}")
    assert q.solve([2]) == 1.0


def test_example2_2():
    q = ClozeQuestion("{1:NUMERICAL:~%100%2:0}")
    assert q.solve([666]) == 0.0


def test_example_negatives():
    q = ClozeQuestion("{1:NUMERICAL:~%100%2:0~%-50%*}")
    assert q.solve([666]) == -0.5
