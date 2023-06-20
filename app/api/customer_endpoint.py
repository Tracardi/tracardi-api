from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException
from pytimeparse.timeparse import timeparse

from tracardi.domain.consent_type import ConsentType
from tracardi.domain.payload.customer_consent import CustomerConsent
from tracardi.domain.profile import Profile, ConsentRevoke
from tracardi.service.storage.driver.elastic import session as session_db
from tracardi.service.storage.driver.elastic import event_source as event_source_db
from tracardi.service.storage.driver.elastic import profile as profile_db
from tracardi.service.storage.driver.elastic import consent_type as consent_type_db

router = APIRouter()


@router.post("/customer/consent", tags=["customer"])
async def add_consent_type(data: CustomerConsent, all: Optional[bool] = False):
    """
    Adds customer consent
    """
    session = await session_db.load_by_id(data.session.id)
    profile = await profile_db.load_by_id(data.profile.id)
    source = await event_source_db.load(data.source.id)

    if not source or not profile or not session:
        raise HTTPException(status_code=403, detail="Access denied")

    profile = profile.to_entity(Profile)
    if all:
        for consent in await consent_type_db.load_all():
            consent_type = ConsentType(**consent)

            if consent_type.auto_revoke:
                try:
                    seconds = timeparse(consent_type.auto_revoke)
                    now = datetime.utcnow()
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
    return await profile_db.save(profile)
