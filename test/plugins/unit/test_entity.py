from tracardi.domain.entity import Entity
from tracardi.domain.storage_record import RecordMetadata


def test_should_set_entity_data():
    entity = Entity(id='1')
    entity.set_meta_data(RecordMetadata(id="1", index="index"))

    assert entity.id == "1"
    assert entity.get_meta_data().id == "1"
    assert entity.get_meta_data().index == "index"


def test_should_accept_empty_meta_data():
    entity = Entity(id='1')

    assert entity.id == "1"
    assert entity.get_meta_data() is None
