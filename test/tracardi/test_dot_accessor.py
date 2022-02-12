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


def test_should_cast_values():
    dot = DotAccessor(
        profile={"a": "1", "b": "false"},
        session={"f": "true"},
        event={"c": "null", "d": "None", "e": {"key": "1.02"}}
    )

    casted_true_value = dot["`true`"]
    true_string = dot["true"]
    casted_false_value = dot["`false`"]
    false_string = dot["false"]
    casted_null_value = dot["`null`"]
    null_string = dot["null"]
    casted_none_value = dot["`none`"]
    none_string = dot["none"]
    casted_int_value = dot["`10`"]
    int_string = dot["10"]
    casted_float_value = dot["`4.16`"]
    float_string = dot["4.16"]
    a = dot["profile@a"]
    a_casted = dot["`profile@a`"]
    b = dot["profile@b"]
    b_casted = dot["`profile@b`"]
    c = dot["event@c"]
    c_casted = dot["`event@c`"]
    d = dot["event@d"]
    d_casted = dot["`event@d`"]
    e = dot["event@e.key"]
    e_casted = dot["`event@e.key`"]
    f = dot["session@f"]
    f_casted = dot["`session@f`"]

    assert a == "1"
    assert a_casted == 1
    assert b == "false"
    assert b_casted is False
    assert c == "null"
    assert c_casted is None
    assert d == "None"
    assert d_casted is None
    assert e == "1.02"
    assert e_casted == 1.02
    assert f == "true"
    assert f_casted is True
    assert casted_true_value is True
    assert casted_false_value is False
    assert casted_null_value is None
    assert casted_none_value is None
    assert casted_int_value == 10
    assert casted_float_value == 4.16
    assert true_string == "true"
    assert false_string == "false"
    assert null_string == "null"
    assert none_string == "none"
    assert int_string == "10"
    assert float_string == "4.16"
