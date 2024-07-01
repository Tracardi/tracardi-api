from time import sleep

import asyncio

from tracardi.context import ServerContext, Context
from test.utils import get_test_tenant
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.service.track_event import track_event

from uuid import uuid4
from test.utils import Endpoint

from test.api.endpoints.test_event_source_endpoint import _create_event_source

endpoint = Endpoint()


async def create_duplicates():
    with ServerContext(Context(production=False, tenant=get_test_tenant())):
        source_id = str(uuid4())

        status = _create_event_source(source_id, "rest").status_code

        assert status == 200

        # Duplicate profile

        events = [
            # {
            #     "source": {
            #         "id": source_id
            #     },
            #     "profile": {
            #         "id": str(uuid4()),
            #         "ids": ['x'],
            #         "metadata": {
            #             "create": "2020-01-01 00:00:00",
            #             "insert": "2020-01-01 00:00:01",
            #             "update": "2020-01-01 00:00:01"
            #         }
            #     },
            #     "session": {
            #         "id": str(uuid4())
            #     },
            #     "events": [
            #         {
            #             "type": "profile-traits-update",
            #             "properties": {
            #                 "traits": {
            #                     "test": 1,
            #                     "test1": 2
            #                 }
            #             }
            #         }
            #     ]
            # },
            {
                "source": {
                    "id": source_id
                },
                "profile": {
                    "id": str(uuid4()),
                    "ids": ['x']
                },
                "session": {
                    "id": str(uuid4())
                },
                "events": [
                    {
                        "type": "profile-update",
                        "properties": {
                            "pii": {
                                "firstname": "Risto",
                                "lastname": "Kowaczewski",
                                "display_name": "Risto Kowaczewski",
                                # "birthday": "2010-01-01 00:00:00",
                                # "language": {
                                #     "native": "string",
                                #     "spoken": [
                                #         "polish"
                                #     ]
                                # },
                            },
                            "media": {
                                "image": ""
                            }
                        }
                    }
                ]
            },
            # {
            #     "source": {
            #         "id": source_id
            #     },
            #     "profile": {
            #         "id": str(uuid4()),
            #         "ids": ['x']
            #     },
            #     "session": {
            #         "id": str(uuid4())
            #     },
            #     "events": [
            #         {
            #             "type": "profile-update",
            #             "properties": {
            #                 "pii": {
            #                     "display_name": "new-display",
            #                     "language": {
            #                         "native": "string",
            #                         "spoken": [
            #                             "spanish"
            #                         ]
            #                     }
            #                 }
            #             }
            #         }
            #     ]
            # },
            # {
            #     "source": {
            #         "id": source_id
            #     },
            #     "profile": {
            #         "id": str(uuid4()),
            #         "ids": ['x']
            #     },
            #     "session": {
            #         "id": str(uuid4())
            #     },
            #     "events": [
            #         {
            #             "type": "increase-interest",
            #             "properties": {
            #                 "interest": "i2",
            #                 "value": 1
            #             }
            #         }
            #     ]
            # },
            # {
            #     "source": {
            #         "id": source_id
            #     },
            #     "profile": {
            #         "id": str(uuid4()),
            #         "ids": ['x']
            #     },
            #     "session": {
            #         "id": str(uuid4())
            #     },
            #     "events": [
            #         {
            #             "type": "increase-interest",
            #             "properties": {
            #                 "interest": "i1",
            #                 "value": 2
            #             }
            #         }
            #     ]
            # }
        ]

        for event in events:
            tracker_payload = TrackerPayload(**event)

            response = await track_event(
                tracker_payload,
                '0.0.0.0',
                allowed_bridges=['rest']
            )
            sleep(.1)
            print(response)


asyncio.run(create_duplicates())
