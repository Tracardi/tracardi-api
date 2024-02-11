Your task is to document errors in code based on the code logic and error numer.

This is the example of how we repoer errors in code.

```python
logger.warning(
    'Security risk. Env AUTO_PROFILE_MERGING is too short. It must be at least 20 chars long.',
    extra=ExtraInfo.build(object=self, origin="configuration", error_number="C0004")
)
```

THis is a standard way of logging errors. The example is a warning that has ExtraInfo. Origin describes the origin of
the error in this example it is configuration. It also gives this error a number.
If the Extra info has more ata like in this example:

```python
extra = ExtraInfo.build(
    origin="workflow",
    event_id=event_id,
    node_id=None,  # We do not know node id here as WF did not start
    flow_id=flow_id,
    profile_id=get_entity_id(self.profile),
    object=self,
    traceback=get_traceback(e),
    error_number="R0003"
)
```

it shows that this error can be connected to event (event_id=event_id), workflow because (flow_id=flow_id), and profile.
This means that this error will be visible if the error logs of events, profiles, and workflow. Please mention it in
description so user can quickly connect error with the send data.

# Your Task

Scan the code delivered below look for the reported errors and create the documentation in the flowing form. Use simple
words (no fancy words) to describe the error. Here is the
template In curly brackets are the tasks for you to generate or fetch content.

# Template

```md
# {error_level}: {message}

Code: {error-number}
Origin: {error-origin}
Level: {error_level}

## Description:

{description when this error is logged. What is it origin. What logic caused to log this error. If there are some
comments use them to better describe the error.}

## Solution

{Describe what to do to solve this error. If you do not know do not put this section (## Solution) in the documentation.
If there are some comments use them to better describe the solution and what should the user do.}
```

# Code

Here is a code to scan for logged errors that need to be documented.

```python
from typing import Optional, TypeVar, Type, Set
from uuid import uuid4
from pydantic import BaseModel, PrivateAttr

from tracardi.domain import ExtraInfo
from tracardi.domain.storage_record import RecordMetadata, StorageRecord
from tracardi.domain.value_object.storage_info import StorageInfo
from tracardi.exceptions.log_handler import get_logger
from tracardi.protocol.operational import Operational
from tracardi.service.dot_notation_converter import dotter
from tracardi.service.storage.index import Resource

logger = get_logger(__name__)

T = TypeVar("T")


class Creatable(BaseModel):

    @classmethod
    def create(cls: Type[T], record: Optional[StorageRecord]) -> Optional[T]:
        if not record:
            return None

        obj = cls(**dict(record))

        if hasattr(obj, 'set_meta_data'):
            obj.set_meta_data(record.get_meta_data())
        return obj


class NullableEntity(Creatable):
    id: Optional[str] = None


class Entity(Creatable):
    id: str
    _metadata: Optional[RecordMetadata] = PrivateAttr(None)

    def set_meta_data(self, metadata: RecordMetadata = None) -> 'Entity':
        self._metadata = metadata
        return self

    def get_meta_data(self) -> Optional[RecordMetadata]:
        return self._metadata if isinstance(self._metadata, RecordMetadata) else None

    def _fill_meta_data(self, index_type: str):
        """
        Used to fill metadata with default current index and id.
        """
        if not self.has_meta_data():
            resource = Resource()
            self.set_meta_data(RecordMetadata(id=self.id, index=resource[index_type].get_write_index()))

    def dump_meta_data(self) -> Optional[dict]:
        return self._metadata.model_dump(mode='json') if isinstance(self._metadata, RecordMetadata) else None

    def has_meta_data(self) -> bool:
        return self._metadata is not None

    def to_storage_record(self, exclude=None, exclude_unset: bool = False) -> StorageRecord:
        record = StorageRecord(**self.model_dump(exclude=exclude, exclude_unset=exclude_unset))

        # Storage records must have ES _id

        if 'id' in record:
            record['_id'] = record['id']

        if self._metadata:
            record.set_meta_data(self._metadata)
        else:
            # Does not have metadata
            storage_info = self.storage_info()  # type: Optional[StorageInfo]
            if storage_info and storage_info.multi is True:
                if isinstance(self, Operational):
                    if self.operation.new is False:
                        # This is critical error of the system. It should be reported to the vendor.
                        logger.error(
                            f"Entity {type(self)} does not have index set. And it is not new.",
                            extra=ExtraInfo.build(object=self, origin="storage", error_number="S0001")
                        )
                else:
                    # This is critical warning of the system. It should be reported to the vendor.
                    logger.warning(
                        f"Entity {type(self)} converts to index-less storage record.",
                        extra=ExtraInfo.build(object=self, origin="storage", error_number="S0002")
                    )
        return record

    @staticmethod
    def new() -> 'Entity':
        return Entity(id=str(uuid4()))

    @staticmethod
    def storage_info() -> Optional[StorageInfo]:
        return None

    def get_dotted_properties(self) -> Set[str]:
        return dotter(self.model_dump())

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id if isinstance(other, Entity) else False


```
