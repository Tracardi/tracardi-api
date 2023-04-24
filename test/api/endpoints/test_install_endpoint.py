from test.utils import Endpoint

endpoint = Endpoint(auth=False)


def test_should_check_if_system_installed():
    response = endpoint.get("/install")
    result = response.json()
    assert 'schema_ok' in result
    assert 'admin_ok' in result


def test_should_not_install_system():
    response = endpoint.post("/install", data={
        "username": 'a@a.pl',
        "password": "a",
        "token": "",
        "needs_admin": True
    })
    assert response.status_code == 403
    result = response.json()
    assert 'created' not in result
    assert 'plugins' not in result
    assert 'admin' not in result


def test_should_install_system():
    response = endpoint.post("/install", data={
        "username": 'a@a.pl',
        "password": "a",
        "token": "tracardi",
        "needs_admin": True
    })
    result = response.json()
    assert 'created' in result[0]  # Staging env
    assert 'templates' in result[0]['created']
    assert 'indices' in result[0]['created']
    assert 'aliases' in result[0]['created']
    assert 'plugins' in result[0]
    assert 'admin' in result[0]
    assert isinstance(result[0]['admin'], bool)


def test_should_install_system_plugins():
    response = endpoint.get("/install/plugins")
    result = response.json()
    assert 'registered' in result
    assert isinstance(result['registered'], list)
    assert 'tracardi.process_engine.action.v1.flow.start.start_action' in result['registered']
