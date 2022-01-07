import asyncio
import os
from dotenv import load_dotenv

from tracardi.process_engine.action.v1.connectors.maxmind.geoip.plugin import GeoIPAction
from tracardi_tests.api.test_resource import create_resource

load_dotenv()


def test_plugin_geo_locator():
    assert create_resource("5600c92a-835d-4fbe-a11d-7076fd983434", type="geo locator", config={
        "webservice": {
            "accountId": os.environ['GEO_LOCATOR_ACCOUNT_ID'],
            "license": os.environ['GEO_LOCATOR_LICENSE'],
            "host": 'geolite.info'
        }

    }).status_code == 200

    kwargs = {
        "source": {
            "id": "5600c92a-835d-4fbe-a11d-7076fd983434",
            "name": "geo"
        },
        "ip": "payload@ip"
    }

    async def main():
        geo = await GeoIPAction.build(**kwargs)
        result = await geo.run(payload={"ip": "5.173.252.207"})
        assert result.value['city'] == 'Wroclaw'
        assert result.value['country']['name'] == 'Poland'
        assert result.value['county'] == 'Lower Silesia'
        assert result.value['postal'] == '50-019'
    asyncio.run(main())
