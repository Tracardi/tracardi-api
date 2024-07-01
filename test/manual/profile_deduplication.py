import asyncio

from tracardi.context import ServerContext, Context
from test.utils import get_test_tenant
from com_tracardi.service.merging.facade import compute_one_profile_in_db
from tracardi.service.tracking.storage.profile_storage import load_profile

from datetime import datetime, timedelta
from test.utils import Endpoint

endpoint = Endpoint()
month = datetime.now().month
year = datetime.now().year
prev_month = (datetime.now() - timedelta(days=32)).month


# FIRST CREATE DUPLICATES. YO Can USE create_duplicate_profiles.py

async def should_deduplicate_profile():
    with ServerContext(Context(production=False, tenant=get_test_tenant())):
        profile = await load_profile('a')

        profile, del_ids = await compute_one_profile_in_db(profile)

        print(del_ids)


asyncio.run(should_deduplicate_profile())
