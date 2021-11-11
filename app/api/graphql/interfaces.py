import strawberry


@strawberry.interface
class Entity:
    id: str
