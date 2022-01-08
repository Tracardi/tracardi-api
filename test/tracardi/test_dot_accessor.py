from tracardi.service.notation.dot_accessor import DotAccessor


def test_dot_accessor():
    dot = DotAccessor(profile={"a": 1, "b": [1, 2]}, session={"b": 2}, event={"c": 1})
    a = dot['profile@...']
    b = dot['profile@b.1']
    c = dot['event@...']
    d = dot['profile@a']
    e = dot['string']

    assert a == {"a": 1, "b": [1, 2]}
    assert b == 2
    assert c == {"c": 1}
    assert d == 1
    assert e == 'string'


def test_dot_accessor_fail():
    dot = DotAccessor(profile={"a": 1, "b": [1, 2]}, session={"b": 2}, event={"c": 1})
    a = dot['xxx@...']
    b = dot['xxx@b.1']
    c = dot['']

    assert a == 'xxx@...'
    assert b == 'xxx@b.1'
    assert c == ''
