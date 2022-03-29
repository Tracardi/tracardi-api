from app.api.domain.user_payload import UserPayload
from tracardi.domain.user import User
from tracardi.service.storage.driver import storage


async def update_user(id, user_payload: UserPayload) -> int:
    current_user = await storage.driver.user.get_by_id(id)
    if not current_user:
        raise LookupError(f"User does not exist {id}")

    user = User(**user_payload.dict(), id=user_payload.email, token=current_user["token"])

    if user_payload.password != current_user["password"]:
        user.encode_password()

    result = await storage.driver.user.update_user(user)
    await storage.driver.user.refresh()

    return result.saved
