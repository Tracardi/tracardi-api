from typing import Optional

from fastapi import APIRouter
from tracardi.service.license import License
from tracardi.domain.payload.customer_consent import CustomerConsent

if License.has_license():
    from com_tracardi.service.consent.consent_manager import add_consent
else:
    from tracardi.service.consent.consent_manager import add_consent

router = APIRouter()


@router.post("/customer/consent", tags=["customer"])
async def add_consent_type(data: CustomerConsent, all: Optional[bool] = False):
    """
    Adds customer consent
    """
    print(data)
    await add_consent(data, all)
