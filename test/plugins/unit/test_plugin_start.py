from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.debug_payload_action import DebugPayloadAction
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.process_engine.action.v1.flow.start.start_action import StartAction
from tracardi.domain.profile import Profile
from tracardi.service.plugin.service.plugin_runner import run_plugin
from tracardi.service.wf.service.builders import action
from tracardi.service.wf.utils.dag_processor import DagProcessor
from tracardi.service.wf.utils.flow_graph_converter import FlowGraphConverter


def test_plugin_start():
    init = {}
    payload = {}
    debug = action(DebugPayloadAction, {
        "event": {
            "type": "page-view",
        }
    })
    start = action(StartAction)
    increase_views = action(IncreaseViewsAction)
    end = action(EndAction)

    flow = Flow.build("End2End - flow", id="1")
    flow += debug("event") >> start('payload')
    flow += start('payload') >> increase_views('payload')
    flow += increase_views('payload') >> end('payload')

    converter = FlowGraphConverter(flow.flowGraph.dict())
    dag_graph = converter.convert_to_dag_graph()
    dag = DagProcessor(dag_graph)

    exec_dag = dag.make_execution_dag(debug=False)
    node = exec_dag.graph[1]

    result = run_plugin(StartAction, init, payload, profile=Profile(id="1"), flow=flow, node=node)
    assert result.output.value == {}
    assert result.output.port == 'payload'
