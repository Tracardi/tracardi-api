"""
Identity Resolution API Endpoints

Authenticated API endpoints for external identity resolution.
Requires admin or developer role.

SECURITY:
- OAuth2 token authentication required
- Role-based access control (admin, developer)
- Audit logging for all operations
- Tenant isolation enforced
"""

from typing import List, Tuple, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from tracardi.domain.identity_resolution_payload import (
    IdentityResolutionResponse,
    ProfileSummary
)
from tracardi.service.identity_resolution_service import IdentityResolutionService
from tracardi.domain.profile import Profile
from tracardi.config import tracardi
from .auth.permissions import Permissions

# Router with authentication - requires admin or developer role
router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
    tags=["identity-resolution"]
)


def _profile_to_summary(profile: Profile) -> ProfileSummary:
    """Convert Profile to ProfileSummary for API response"""
    return ProfileSummary(
        id=profile.id,
        ids=profile.ids,
        traits=profile.traits,
        created=str(profile.metadata.time.insert) if profile.metadata.time.insert else None,
        updated=str(profile.metadata.time.update) if profile.metadata.time.update else None,
        segments=profile.segments
    )


@router.post(
    "/identity-resolution/validate-profile",
    response_model=dict,
    include_in_schema=tracardi.expose_gui_api
)
async def validate_profile(profile_id: str):
    """
    Validate if a profile ID exists and is usable.
    
    **CRITICAL**: Use this endpoint before tracking events to ensure 
    you're using the correct profile ID after merge operations.
    
    **Permissions**: admin, developer
    
    **Returns**:
    - is_valid: True if profile exists and is active
    - profile_id: Current active profile ID (may differ if merged)
    - error: Error description if not valid
    - message: Human-readable message
    
    **Example**:
    ```
    GET /identity-resolution/validate-profile?profile_id=profile-456
    ```
    
    **Response (profile is valid)**:
    ```json
    {
        "is_valid": true,
        "profile_id": "profile-456",
        "message": "Profile is valid and active"
    }
    ```
    
    **Response (profile was merged)**:
    ```json
    {
        "is_valid": false,
        "profile_id": "profile-123",
        "error": "Profile profile-456 was merged into profile-123",
        "message": "Use profile-123 in tracker payloads"
    }
    ```
    """
    try:
        is_valid, actual_id, error = await IdentityResolutionService.validate_profile_id(profile_id)
        
        if is_valid:
            return {
                "is_valid": True,
                "profile_id": actual_id,
                "message": "Profile is valid and active"
            }
        else:
            return {
                "is_valid": False,
                "profile_id": actual_id,
                "error": error,
                "message": f"Use {actual_id} in tracker payloads" if actual_id else "Profile not found"
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )


@router.post(
    "/identity-resolution/merge-by-ids",
    response_model=IdentityResolutionResponse,
    include_in_schema=tracardi.expose_gui_api
)
async def merge_profiles_by_ids(
    primary_profile_id: str,
    additional_profile_ids: List[str],
    validate_circular: bool = True,
    validate_resurrection: bool = True
):
    """
    Merge multiple profiles by their IDs.
    
    **CRITICAL**: After using this API:
    1. Use the returned `merged_profile_id` in all subsequent tracker payloads
    2. Set `externalIdentityResolution: true` in tracker payload options
    3. Validate profile IDs with `/validate-profile` endpoint before tracking
    
    **DO NOT** use old profile IDs after merge - they will not be found!
    
    **Permissions**: admin, developer
    
    **Parameters**:
    - primary_profile_id: The main profile ID to merge others into
    - additional_profile_ids: List of profile IDs to merge with primary
    - validate_circular: Check for circular merge chains (default: true)
    - validate_resurrection: Check for zombie profiles (default: true)
    
    **Example**:
    ```json
    {
        "primary_profile_id": "profile-123",
        "additional_profile_ids": ["profile-456", "profile-789"],
        "validate_circular": true,
        "validate_resurrection": true
    }
    ```
    
    **Response**:
    ```json
    {
        "success": true,
        "merged_profile_id": "profile-123",
        "merged_profile_ids": ["profile-123", "profile-456", "profile-789"],
        "message": "Successfully merged 3 profiles",
        "profile": {
            "id": "profile-123",
            "ids": ["profile-123", "profile-456", "profile-789"],
            "traits": {...}
        }
    }
    ```
    """
    try:
        # Validate primary profile exists
        is_valid, actual_id, error = await IdentityResolutionService.validate_profile_id(
            primary_profile_id
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Primary profile validation failed: {error}. " +
                       (f"Use {actual_id} instead" if actual_id else "Profile not found")
            )
        
        # Perform merge with safety checks
        merged_profile = await IdentityResolutionService.resolve_by_profile_ids(
            primary_profile_id=primary_profile_id,
            additional_profile_ids=additional_profile_ids,
            validate_circular=validate_circular,
            validate_resurrection=validate_resurrection
        )
        
        if merged_profile:
            return IdentityResolutionResponse(
                success=True,
                merged_profile_id=merged_profile.id,
                merged_profile_ids=merged_profile.ids,
                message=f"Successfully merged {len(merged_profile.ids)} profiles",
                profile=_profile_to_summary(merged_profile)
            )
        else:
            return IdentityResolutionResponse(
                success=False,
                message="No profiles to merge or merge not needed"
            )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Identity resolution failed: {str(e)}"
        )


@router.post(
    "/identity-resolution/merge-by-keys",
    response_model=IdentityResolutionResponse,
    include_in_schema=tracardi.expose_gui_api
)
async def merge_profiles_by_keys(
    profile_id: str,
    merge_keys: List[Tuple[str, str]]
):
    """
    Merge profiles by matching key-value pairs.
    
    Common use cases: merge by email, phone number, or custom identifier.
    
    **CRITICAL**: After merge, use the returned `merged_profile_id` and set 
    `externalIdentityResolution: true` in tracker payloads.
    
    **Permissions**: admin, developer
    
    **Parameters**:
    - profile_id: Primary profile ID
    - merge_keys: List of (field, value) tuples to match profiles
      Example: [("data.contact.email.main", "user@example.com")]
    
    **Example**:
    ```json
    {
        "profile_id": "profile-123",
        "merge_keys": [
            ["data.contact.email.main", "user@example.com"]
        ]
    }
    ```
    
    **Multiple keys example**:
    ```json
    {
        "profile_id": "profile-123",
        "merge_keys": [
            ["data.contact.email.main", "user@example.com"],
            ["data.contact.phone.main", "+1234567890"]
        ]
    }
    ```
    """
    try:
        # Validate profile exists
        is_valid, actual_id, error = await IdentityResolutionService.validate_profile_id(profile_id)
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Profile validation failed: {error}. " +
                       (f"Use {actual_id} instead" if actual_id else "Profile not found")
            )
        
        # Perform merge
        merged_profile = await IdentityResolutionService.resolve_by_merge_keys(
            profile_id=profile_id,
            merge_keys=merge_keys
        )
        
        if merged_profile:
            return IdentityResolutionResponse(
                success=True,
                merged_profile_id=merged_profile.id,
                merged_profile_ids=merged_profile.ids,
                message=f"Successfully merged {len(merged_profile.ids)} profiles",
                profile=_profile_to_summary(merged_profile)
            )
        else:
            return IdentityResolutionResponse(
                success=False,
                message="No profiles to merge or merge not needed"
            )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Identity resolution failed: {str(e)}"
        )


@router.post(
    "/identity-resolution/merge-by-field",
    response_model=IdentityResolutionResponse,
    include_in_schema=tracardi.expose_gui_api
)
async def merge_profiles_by_field(
    field_name: str,
    field_value: str,
    primary_profile_id: Optional[str] = None
):
    """
    Convenience endpoint to merge profiles by a single field value.
    
    This is a simplified version of merge-by-keys for single field matching.
    
    **Permissions**: admin, developer
    
    **Parameters**:
    - field_name: Profile field name (e.g., 'data.contact.email.main')
    - field_value: Value to match
    - primary_profile_id: Optional primary profile ID. If not provided,
                         the newest profile will be used as primary.
    
    **Example**:
    ```json
    {
        "field_name": "data.contact.email.main",
        "field_value": "user@example.com",
        "primary_profile_id": "profile-123"
    }
    ```
    """
    try:
        merged_profile = await IdentityResolutionService.resolve_by_field_value(
            field_name=field_name,
            field_value=field_value,
            primary_profile_id=primary_profile_id
        )
        
        if merged_profile:
            return IdentityResolutionResponse(
                success=True,
                merged_profile_id=merged_profile.id,
                merged_profile_ids=merged_profile.ids,
                message=f"Successfully merged {len(merged_profile.ids)} profiles",
                profile=_profile_to_summary(merged_profile)
            )
        else:
            return IdentityResolutionResponse(
                success=False,
                message="No profiles to merge or merge not needed"
            )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Identity resolution failed: {str(e)}"
        )


@router.post(
    "/identity-resolution/find-duplicates",
    response_model=dict,
    include_in_schema=tracardi.expose_gui_api
)
async def find_duplicate_profiles(
    merge_keys: List[Tuple[str, str]],
    limit: int = 1000
):
    """
    Find duplicate profiles matching the given keys without performing merge.
    
    This is useful for preview/analysis before performing actual merge.
    You can review the duplicate profiles and then decide whether to merge them.
    
    **Permissions**: admin, developer
    
    **Parameters**:
    - merge_keys: List of (field, value) tuples to find duplicate profiles
    - limit: Maximum number of profiles to return (default: 1000)
    
    **Example**:
    ```json
    {
        "merge_keys": [
            ["data.contact.email.main", "user@example.com"]
        ],
        "limit": 100
    }
    ```
    
    **Response**:
    ```json
    {
        "success": true,
        "count": 3,
        "profiles": [
            {
                "id": "profile-123",
                "ids": ["profile-123"],
                "traits": {...}
            }
        ],
        "message": "Found 3 duplicate profiles"
    }
    ```
    """
    try:
        profiles = await IdentityResolutionService.find_duplicate_profiles(
            merge_keys=merge_keys,
            limit=limit
        )
        
        profile_summaries = [_profile_to_summary(p) for p in profiles]
        
        return {
            "success": True,
            "count": len(profiles),
            "profiles": profile_summaries,
            "message": f"Found {len(profiles)} duplicate profiles"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find duplicates: {str(e)}"
        )


@router.post(
    "/identity-resolution/detect-circular-merge",
    response_model=dict,
    include_in_schema=tracardi.expose_gui_api
)
async def detect_circular_merge(
    profile_id: str,
    max_depth: int = 10
):
    """
    Detect circular merge chains before they cause data corruption.
    
    Example circular chain: A→B→C→A
    
    **CRITICAL**: Always call this before merge operations to prevent data corruption.
    
    **Permissions**: admin, developer
    
    **Parameters**:
    - profile_id: Starting profile ID to check
    - max_depth: Maximum chain depth to check (default: 10)
    
    **Response (no circle)**:
    ```json
    {
        "has_circle": false,
        "chain": ["profile-A", "profile-B", "profile-C"],
        "message": "No circular merge detected"
    }
    ```
    
    **Response (circle detected)**:
    ```json
    {
        "has_circle": true,
        "chain": ["profile-A", "profile-B", "profile-C", "profile-A"],
        "message": "Circular merge detected: profile-A → profile-B → profile-C → profile-A"
    }
    ```
    """
    try:
        has_circle, chain = await IdentityResolutionService.detect_circular_merge(
            profile_id=profile_id,
            max_depth=max_depth
        )
        
        if has_circle:
            return {
                "has_circle": True,
                "chain": chain,
                "message": f"Circular merge detected: {' → '.join(chain)}"
            }
        else:
            return {
                "has_circle": False,
                "chain": chain,
                "message": "No circular merge detected"
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Circular merge detection failed: {str(e)}"
        )


@router.post(
    "/identity-resolution/check-resurrection",
    response_model=dict,
    include_in_schema=tracardi.expose_gui_api
)
async def check_profile_resurrection(profile_id: str):
    """
    Check if profile ID was previously used and merged (zombie profile detection).
    
    This prevents accidentally creating a new profile with an ID that was
    previously merged, which would create duplicate/inconsistent data.
    
    **Permissions**: admin, developer
    
    **Parameters**:
    - profile_id: Profile ID to check
    
    **Response (not resurrected)**:
    ```json
    {
        "is_resurrected": false,
        "merged_into": null,
        "message": "Profile ID is safe to use"
    }
    ```
    
    **Response (resurrected - zombie profile)**:
    ```json
    {
        "is_resurrected": true,
        "merged_into": "profile-123",
        "message": "WARNING: profile-456 was previously merged into profile-123"
    }
    ```
    """
    try:
        is_resurrected, merged_into = await IdentityResolutionService.check_profile_resurrection(
            profile_id=profile_id
        )
        
        if is_resurrected:
            return {
                "is_resurrected": True,
                "merged_into": merged_into,
                "message": f"WARNING: {profile_id} was previously merged into {merged_into}"
            }
        else:
            return {
                "is_resurrected": False,
                "merged_into": None,
                "message": "Profile ID is safe to use"
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Resurrection check failed: {str(e)}"
        )
