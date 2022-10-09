from test.utils import Endpoint

endpoint = Endpoint()


def _add_user_preference(preference=None):
    if preference is None:
        preference = {
            "test_1": "preference_1",
            "test_2": "preference_2"
        }
        response = endpoint.post("/user/preference/test_preference", preference)
        assert response.status_code == 200

        return response


def test_should_return_user_preference_by_given_key():
    try:
        _add_user_preference()

        result = endpoint.get("/user/preference/test_preference")
        result = result.json()

        assert result["test_1"] == "preference_1"
        assert result["test_2"] == "preference_2"
    finally:
        endpoint.delete("/user/preference/test_preference")


def test_should_delete_preference():
    try:
        _add_user_preference()

        result = endpoint.delete("/user/preference/test_preference")
        assert result.status_code == 200
        result = result.json()

        assert result["saved"] == 1

    finally:
        endpoint.delete("/user/preference/test_preference")


def test_should_set_new_preferences():
    new_preferences = {
        "test_3": "preference_3",
        "test_4": "preference_4"
    }
    try:

        endpoint.post("/user/preference/test_preference", new_preferences)

        result = endpoint.get("/user/preferences")
        result = result.json()

        assert result['test_preference']['test_3'] == "preference_3"
        assert result['test_preference']['test_4'] == "preference_4"

    finally:
        endpoint.delete("/user/preference/test_preference")


def test_should_return_all_preferences():
    try:
        _add_user_preference()

        result = endpoint.get("/user/preferences")
        result = result.json()

        assert result['test_preference']['test_1'] == "preference_1"
        assert result['test_preference']['test_2'] == "preference_2"

    finally:
        endpoint.delete("/user/preference/test_preference")
