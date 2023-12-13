from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException
from pytimeparse.timeparse import timeparse

from tracardi.service.tracking.cache.profile_cache import save_profile_cache
from tracardi.service.tracking.storage.profile_storage import load_profile, save_profile
from tracardi.service.tracking.storage.session_storage import load_session
from tracardi.service.utils.date import now_in_utc
from tracardi.domain.consent_type import ConsentType
from tracardi.domain.payload.customer_consent import CustomerConsent
from tracardi.domain.profile import ConsentRevoke
from tracardi.service.storage.driver.elastic import event_source as event_source_db
from tracardi.service.storage.driver.elastic import consent_type as consent_type_db


router = APIRouter()


@router.post("/customer/consent", tags=["customer"])
async def add_consent_type(data: CustomerConsent, all: Optional[bool] = False):
    """
    Adds customer consent
    """
    session = await load_session(data.session.id)
    profile = await load_profile(data.profile.id)
    source = await event_source_db.load(data.source.id)

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

    profile.aux['consents'] = {"displayed": True}

    save_profile_cache(profile)
    return await save_profile(profile)
