from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_status_200_if_validated():
    response = endpoint.request("/tql/validate", "profile@id exists")
    if response.status_code != 200:
        print(response.content)
    assert response.status_code == 200


def test_should_return_status_400_if_not_validated():
    response = endpoint.request("/tql/validate", "test_wrong_data")
    assert response.status_code == 400
