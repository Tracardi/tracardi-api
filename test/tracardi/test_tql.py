from tracardi.domain.event_metadata import EventMetadata, EventTime
from tracardi.service.notation.dot_accessor import DotAccessor
from tracardi.domain.profile import Profile
from tracardi.domain.context import Context
from tracardi.domain.event import Event, EventSession
from tracardi.domain.flow import Flow, FlowSchema
from tracardi.domain.resource import Resource
from tracardi.process_engine.tql.parser import Parser
from tracardi.process_engine.tql.transformer.expr_transformer import ExprTransformer

payload = {
    "a": {
        "b": 1,
        "c": [1, 2, 3],
        "d": {"aa": 1},
        "e": "test",
        'f': 1,
        'g': True,
        'h': None,
        'i': "2021-01-10"
    }
}

profile = Profile(id="1")
session = EventSession(id="2")
resource = Resource(id="3", type="event")
context = Context()
event = Event(id="event-id",
              type="type",
              metadata=EventMetadata(time=EventTime()),
              source=resource,
              context=context,
              profile=profile,
              session=session,
              )
flow = Flow(id="flow-id", name="flow", wf_schema=FlowSchema(version="0.g.0"))
dot = DotAccessor(profile, session, payload, event, flow)

parser = Parser(Parser.read('grammar/uql_expr.lark'), start='expr')


def test_tql_between():
    tree = parser.parse("payload@a.d.aa between 1 and 2")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_equal():
    tree = parser.parse("payload@a.e == \"test\"")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.b == payload@a.f")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.g == True")
    assert ExprTransformer(dot=dot).transform(tree)

    # Not allowed
    # tree = parser.parse("payload@a.h == null")
    # assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.b == 1")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_greater_then():
    tree = parser.parse("payload@a.b >= 1")
    assert ExprTransformer(dot=dot).transform(tree)
    tree = parser.parse("payload@a.b > 0")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_lower_then():
    tree = parser.parse("payload@a.b <= 1")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.b < 2")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_equal_date():
    tree = parser.parse("datetime(payload@a.i) == datetime(\"2021-01-10\")")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) <= datetime(\"2021-01-10\")")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) >= datetime(\"2021-01-10\")")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) < datetime(\"2021-01-11\")")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) > datetime(\"2021-01-09\")")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) < datetime(\"2021-01-10 00:00:01\")")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) between datetime(\"2020-01-01\") and datetime(\"2022-01-01\")")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_is():
    tree = parser.parse("payload@a.h is null")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_exists():
    tree = parser.parse("payload@a.h exists")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.h.h not exists")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_false_between():
    tree = parser.parse("payload@a.d.aa between 3 and 4")
    assert not ExprTransformer(dot=dot).transform(tree)


def test_tql_false_not_equal():
    tree = parser.parse("payload@a.e != \"test\"")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.b != payload@a.f")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.g != True")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.b != 1")
    assert not ExprTransformer(dot=dot).transform(tree)


# todo not working
# def test_tql_false_is_not():
#     tree = parser.parse("payload@a.h is not null")
#     assert not ExprTransformer(dot=dot).transform(tree)


def test_tql_false_greater_then():
    tree = parser.parse("payload@a.b > 1")
    assert not ExprTransformer(dot=dot).transform(tree)
    tree = parser.parse("payload@a.b > 0")
    assert ExprTransformer(dot=dot).transform(tree)


def test_tql_false_lower_then():
    tree = parser.parse("payload@a.b < 1")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.b > 2")
    assert not ExprTransformer(dot=dot).transform(tree)


def test_tql_false_date_ops():
    tree = parser.parse("datetime(payload@a.i) != datetime(\"2021-01-10\")")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) < datetime(\"2021-01-10\")")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) > datetime(\"2021-01-10\")")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) > datetime(\"2021-01-11\")")
    assert not ExprTransformer(dot=dot).transform(tree)
    #
    tree = parser.parse("datetime(payload@a.i) < datetime(\"2021-01-09\")")
    assert not ExprTransformer(dot=dot).transform(tree)
    #
    tree = parser.parse("datetime(payload@a.i) > datetime(\"2021-01-10 00:00:01\")")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("datetime(payload@a.i) between datetime(\"2022-01-01\") and datetime(\"2023-01-01\")")
    assert not ExprTransformer(dot=dot).transform(tree)


def test_tql_datetime_now():
    tree = parser.parse("now() == now()")
    assert not ExprTransformer(dot=dot).transform(tree)


def test_tql_false_exists():
    tree = parser.parse("payload@a.h not exists")
    assert not ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.h.h exists")
    assert not ExprTransformer(dot=dot).transform(tree)


def test_tql_bool_operations():
    tree = parser.parse("payload@a.d.aa between 1 and 2 and payload@a.e == \"test\"")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.d.aa between 1 and 2 or payload@a.e != \"test\"")
    assert ExprTransformer(dot=dot).transform(tree)

    tree = parser.parse("payload@a.d.aa between 2 and 3 and payload@a.e != \"test\"")
    assert not ExprTransformer(dot=dot).transform(tree)


def test_tql_fail():
    try:
        tree = parser.parse("a.b > 1")
        ExprTransformer(dot=dot).transform(tree)
        assert False
    except Exception:
        assert True

    try:
        tree = parser.parse("payload@... > 1")
        ExprTransformer(dot=dot).transform(tree)
        assert False
    except Exception:
        assert True

    # todo this could work
    # try:
    #     tree = parser.parse("payload@... exists")
    #     ExprTransformer(dot=dot).transform(tree)
    #     assert False
    # except Exception:
    #     assert True


def test_tql_no_value():
    try:
        tree = parser.parse("payload@no-value.b > 1")
        ExprTransformer(dot=dot).transform(tree)
        assert False
    except Exception as e:
        assert 'Invalid dot notation' in str(e)
