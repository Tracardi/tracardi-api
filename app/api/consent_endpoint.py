from fastapi import APIRouter, Depends, HTTPException
from auth.authentication import get_current_user
from tracardi.domain.consent_schema import ConsentSchema
from uuid import UUID
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException
from app.config import server


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/consent/id/{id}", tags=["consent"], response_model=dict, include_in_schema=server.expose_gui_api)
async def add_consent(id: UUID, consent: ConsentSchema):
    try:
        profile = await storage.driver.profile.load_by_id(str(id))
        if profile is None:
            raise HTTPException(status_code=404, detail=f"Unable to find profile with ID: {str(id)}")
        else:
            profile.consents = list(filter(lambda c: c.type_id != consent.type_id, profile.consents))
            profile.consents.append(consent)
            result = await storage.driver.profile.save_profile(profile)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"updated_profiles": result["saved"]}
