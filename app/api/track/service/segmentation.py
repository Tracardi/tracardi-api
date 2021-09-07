from typing import Callable

from tracardi.domain.profile import Profile


async def segment(profile: Profile, event_types: list, load_segment_by_event_type: Callable) -> dict:
    segmentation_result = {"errors": [], "ids": []}
    try:
        # Segmentation
        if profile.operation.needs_update() or profile.operation.needs_segmentation():

            # Segmentation runs only if profile was updated or flow forced it
            async for event_type, segment_id, error in profile.segment(
                    event_types,
                    load_segment_by_event_type):
                # Segmentation triggered
                if error:
                    segmentation_result['errors'].append(error)
                segmentation_result['ids'].append(segment_id)
    except Exception as e:
        # this error is a global segmentation error
        # todo log it.
        print(str(e))
    finally:
        return segmentation_result
