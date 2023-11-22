# from typing import Tuple
#
# from app.api.domain.user_payload import UserPayload
# from tracardi.domain.user import User
# from tracardi.service.storage.driver.elastic import user as user_db
#
#
# async def update_user(id, user_payload: UserPayload) -> Tuple[int, User]:
#     current_user = await user_db.load_by_id(id)
#     if not current_user:
#         raise LookupError(f"User does not exist {id}")
#
#     user = User(**user_payload.model_dump(),
#                 id=id,
#                 expiration_timestamp=user_payload.get_expiration_date())
#
#     if user_payload.password != current_user["password"]:
#         user.password = User.encode_password(user.password)
#
#     result = await user_db.update_user(user)
#     await user_db.refresh()
#
#     return result.saved, user
