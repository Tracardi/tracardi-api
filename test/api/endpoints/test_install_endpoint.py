from test.utils import Endpoint

endpoint = Endpoint(auth=False)


def test_should_check_if_system_installed():
    response = endpoint.get("/install")
    result = response.json()
    assert 'schema_ok' in result
    assert 'admin_ok' in result


def test_should_install_system():
    response = endpoint.post("/install", data={
        "username": 'a@a.pl',
        "password": "a",
        "token": "",
        "needs_admin": True
    })
    result = response.json()
    assert 'created' in result
    assert 'templates' in result['created']
    assert 'indices' in result['created']
    assert 'aliases' in result['created']
    assert 'plugins' in result
    assert 'admin' in result
    assert isinstance(result['admin'], bool)

    from .test_test_endpoint import _check_if_has_installed_indices
    _check_if_has_installed_indices()


def test_should_install_system_plugins():
    response = endpoint.get("/install/plugins")
    result = response.json()
    assert 'registered' in result
    assert isinstance(result['registered'], list)
    assert 'tracardi.process_engine.action.v1.flow.start.start_action' in result['registered']


