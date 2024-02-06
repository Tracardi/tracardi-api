from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException
from pytimeparse.timeparse import timeparse

from tracardi.service.storage.redis.collections import Collection
from tracardi.service.storage.redis_client import RedisClient
from tracardi.service.tracking.locking import Lock, async_mutex
from tracardi.service.tracking.storage.profile_storage import load_profile, save_profile
from tracardi.service.tracking.storage.session_storage import load_session
from tracardi.service.utils.date import now_in_utc
from tracardi.domain.consent_type import ConsentType
from tracardi.domain.payload.customer_consent import CustomerConsent
from tracardi.domain.profile import ConsentRevoke
from tracardi.service.storage.driver.elastic import event_source as event_source_db
from tracardi.service.storage.driver.elastic import consent_type as consent_type_db
from tracardi.service.utils.getters import get_entity_id

router = APIRouter()


@router.post("/customer/consent", tags=["customer"])
async def add_consent_type(data: CustomerConsent, all: Optional[bool] = False):
    """
    Adds customer consent
    """

    session = await load_session(data.session.id)
    source = await event_source_db.load(data.source.id)

    _redis = RedisClient()
    profile_key = Lock.get_key(Collection.lock_tracker, "profile", get_entity_id(data.profile))
    profile_lock = Lock(_redis, profile_key, default_lock_ttl=3)

    async with async_mutex(profile_lock, name='add_consent_type'):

        profile = await load_profile(data.profile.id)

        if not source or not profile or not session:
            raise HTTPException(status_code=403, detail="Access denied")

        if all:
            for consent in await consent_type_db.load_all():
                consent_type = ConsentType(**consent)

                if consent_type.auto_revoke:
                    try:
                        seconds = timeparse(consent_type.auto_revoke)
                        now = now_in_utc()
                        revoke = now + timedelta(seconds=seconds)
                        revoke = ConsentRevoke(revoke=revoke)
                    except Exception:
                        revoke = ConsentRevoke()

                else:
                    revoke = ConsentRevoke()

                profile.consents[consent['id']] = revoke
        else:
            for consent, flag in data.consents.items():
                if flag:
                    profile.consents[consent] = ConsentRevoke()
                else:
                    if consent in profile.consents:
                        del profile.consents[consent]

        profile.aux['consents'] = {"granted": True}

        return await save_profile(profile, refresh=True)
