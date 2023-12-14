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
from tracardi.service.storage.mysql.mapping.event_source_mapping import map_to_event_source
from tracardi.service.storage.mysql.service.consent_type_service import ConsentTypeService
from tracardi.service.storage.mysql.service.event_source_service import EventSourceService

router = APIRouter()


@router.post("/customer/consent", tags=["customer"])
async def add_consent_type(data: CustomerConsent, all: Optional[bool] = False):
    """
    Adds customer consent
    """
    session = await load_session(data.session.id)
    profile = await load_profile(data.profile.id)
    source = (await EventSourceService().load_by_id(data.source.id)).map_to_object(map_to_event_source)

    if not source or not profile or not session:
        raise HTTPException(status_code=403, detail="Access denied")

    if all:
        cts = ConsentTypeService()
        consent_type_records = await cts.load_all()
        for consent_type in consent_type_records.map_to_object(ConsentType):

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

            profile.consents[consent_type.id] = revoke
    else:
        for consent, flag in data.consents.items():
            if flag:
                profile.consents[consent] = ConsentRevoke()
            else:
                if consent in profile.consents:
                    del profile.consents[consent]

    profile.aux['consents'] = {"granted": True}

    save_profile_cache(profile)
    return await save_profile(profile)
